#!/usr/bin/env bash
# Déploiement de Memaster sur NEAR **testnet** (jamais mainnet), relançable : chaque étape déjà
# faite est sautée (compte existant, contrat déjà initialisé, série déjà chargée ou ouverte).
#
# Prérequis : near-cli-rs (`near`), cargo-near, python3, curl. Les clés sont lues dans
# ~/.near-credentials (trousseau « legacy » de near-cli-rs) : aucune clé n'est lue ni écrite dans le repo.
#
# Variables d'environnement :
#   ROOT_ID              compte racine testnet (owner du contrat, paie les sous-comptes et les séries) — requis
#   NETWORK              doit valoir « testnet » (défaut) ; toute autre valeur est refusée
#   RPC_URL              RPC des vues (défaut https://rpc.testnet.fastnear.com ; rpc.testnet.near.org est déprécié et répond 429)
#   CONTRACT_ID          défaut app.$ROOT_ID
#   REDEEMER_ID          défaut redeemer.$ROOT_ID (mock-redeemer)
#   ORACLE_ID            défaut oracle.$ROOT_ID (mock-oracle, opérateur = ROOT_ID)
#   BUYERS               nombre d'acheteurs de test buyerN.$ROOT_ID (défaut 3)
#   CONTRACT_NEAR        solde initial du contrat (défaut 7 ; le wasm de 551 Ko immobilise ~5,5 NEAR)
#   MOCK_NEAR            solde initial de chaque mock (défaut 1.5)
#   BUYER_NEAR           solde initial de chaque acheteur (défaut 3)
#   REVEAL_STEPS         k (défaut 3)
#   RETRY_DELAY_BLOCKS   délai de retry_reveal (défaut 100, valeur par défaut du contrat)
#   ORACLE_DELAY_BLOCKS  délai d'installation de l'oracle (défaut 30 sur testnet ; 144 000 = 24 h en prod)
#   SERIES_PARAMS        paramètres de build_series.py (défaut scripts/serie-exemple.json)
#   TABLES_VALEUR        tables de valeur passées à build_series.py --tables-valeur (optionnel,
#                        ex. ../sim/resultats/serie5/tables-valeur.json)
#   SERIES_OUT           dossier des arguments générés (défaut scripts/out/<slug>) ; à changer pour
#                        un second contrat, afin de ne pas écraser la table du premier
#   SKIP_BUILD=1         ne pas reconstruire les wasm
#   SKIP_CONTROL=1       ne pas créer la série de contrôle sans mécanique
set -euo pipefail

NETWORK=${NETWORK:-testnet}
[ "$NETWORK" = "testnet" ] || { echo "Refus : ce script ne déploie que sur testnet (NETWORK=$NETWORK)" >&2; exit 1; }
: "${ROOT_ID:?ROOT_ID requis (compte racine .testnet)}"
case "$ROOT_ID" in *.testnet) ;; *) echo "Refus : ROOT_ID doit finir par .testnet" >&2; exit 1;; esac

HERE=$(cd "$(dirname "$0")" && pwd)
CONTRACT_DIR=$(dirname "$HERE")
RPC_URL=${RPC_URL:-https://rpc.testnet.fastnear.com}
CONTRACT_ID=${CONTRACT_ID:-app.$ROOT_ID}
REDEEMER_ID=${REDEEMER_ID:-redeemer.$ROOT_ID}
ORACLE_ID=${ORACLE_ID:-oracle.$ROOT_ID}
BUYERS=${BUYERS:-3}
CONTRACT_NEAR=${CONTRACT_NEAR:-7}
MOCK_NEAR=${MOCK_NEAR:-1.5}
BUYER_NEAR=${BUYER_NEAR:-3}
REVEAL_STEPS=${REVEAL_STEPS:-3}
RETRY_DELAY_BLOCKS=${RETRY_DELAY_BLOCKS:-100}
ORACLE_DELAY_BLOCKS=${ORACLE_DELAY_BLOCKS:-30}
SERIES_PARAMS=${SERIES_PARAMS:-$HERE/serie-exemple.json}
SIGN=(network-config testnet sign-with-legacy-keychain send)

log() { printf '\n== %s\n' "$*"; }

# Vue JSON par RPC (sortie : le résultat décodé, ou « null » si la vue panique ou le compte n'existe pas).
view() {
  python3 - "$RPC_URL" "$1" "$2" "${3:-{\}}" <<'PY'
import base64, json, sys, time, urllib.request
rpc, acc, meth, args = sys.argv[1:5]
body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "query", "params": {
    "request_type": "call_function", "finality": "final", "account_id": acc, "method_name": meth,
    "args_base64": base64.b64encode(args.encode()).decode()}}).encode()
for attempt in range(5):
    try:
        req = urllib.request.Request(rpc, body, {"content-type": "application/json"})
        r = json.load(urllib.request.urlopen(req, timeout=20))
        break
    except Exception:
        time.sleep(2 * (attempt + 1))
else:
    sys.exit("RPC injoignable")
res = r.get("result") or {}
if "result" not in res:
    print("null"); sys.exit(0)
print(bytes(res["result"]).decode())
PY
}
account_exists() {
  python3 - "$RPC_URL" "$1" <<'PY'
import json, sys, urllib.request
rpc, acc = sys.argv[1:3]
body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "query", "params": {
    "request_type": "view_account", "finality": "final", "account_id": acc}}).encode()
r = json.load(urllib.request.urlopen(urllib.request.Request(rpc, body, {"content-type": "application/json"}), timeout=20))
sys.exit(0 if "result" in r else 1)
PY
}
code_hash() {
  python3 - "$RPC_URL" "$1" <<'PY'
import json, sys, urllib.request
rpc, acc = sys.argv[1:3]
body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "query", "params": {
    "request_type": "view_account", "finality": "final", "account_id": acc}}).encode()
r = json.load(urllib.request.urlopen(urllib.request.Request(rpc, body, {"content-type": "application/json"}), timeout=20))
print(r.get("result", {}).get("code_hash", ""))
PY
}
jget() { python3 -c "import json,sys; d=json.load(sys.stdin); print(eval(sys.argv[1], {'d': d}))" "$1"; }
call() { # call <signer> <method> <json-args|@fichier> <gaz Tgas> <dépôt yocto>
  local signer=$1 method=$2 args=$3 gas=$4 dep=$5 a
  if [[ $args == @* ]]; then a=(file-args "${args#@}"); else a=(json-args "$args"); fi
  near contract call-function as-transaction "$CONTRACT_ID" "$method" "${a[@]}" \
    prepaid-gas "$gas Tgas" attached-deposit "$dep yoctonear" sign-as "$signer" "${SIGN[@]}" 2>&1 \
    | grep -E "Transaction ID|rror|panicked|Smart contract" || true
}

# 1. Build
if [ "${SKIP_BUILD:-0}" != 1 ]; then
  log "Build des wasm (non reproductible, voir docs/testnet.md)"
  (cd "$CONTRACT_DIR" && cargo near build non-reproducible-wasm >/dev/null)
  (cd "$CONTRACT_DIR/mock-redeemer" && cargo near build non-reproducible-wasm >/dev/null)
  (cd "$CONTRACT_DIR/mock-oracle" && cargo near build non-reproducible-wasm >/dev/null)
fi
WASM=$CONTRACT_DIR/target/near/memaster.wasm
WASM_REDEEMER=$CONTRACT_DIR/target/near/mock_redeemer/mock_redeemer.wasm
WASM_ORACLE=$CONTRACT_DIR/target/near/mock_oracle/mock_oracle.wasm
shasum -a 256 "$WASM" "$WASM_REDEEMER" "$WASM_ORACLE"

# 2. Comptes
account_exists "$ROOT_ID" || { echo "Compte racine $ROOT_ID introuvable (créer-le avec le faucet)" >&2; exit 1; }
mk_sub() { # mk_sub <compte> <NEAR>
  if account_exists "$1"; then echo "$1 existe"; return; fi
  for attempt in 1 2 3; do
    log "Création de $1 ($2 NEAR), essai $attempt"
    near account create-account fund-myself "$1" "$2 NEAR" autogenerate-new-keypair save-to-legacy-keychain \
      sign-as "$ROOT_ID" "${SIGN[@]}" 2>&1 | grep -E "Transaction ID|created successfully|rror" || true
    sleep 3
    account_exists "$1" && return
    # Échec (vu sur testnet : « Transaction has expired ») : la clé locale générée ne sert à rien.
    rm -rf "$HOME/.near-credentials/testnet/$1" "$HOME/.near-credentials/testnet/$1.json"
    sleep $((attempt * 5))
  done
  echo "Création de $1 impossible" >&2; exit 1
}
mk_sub "$CONTRACT_ID" "$CONTRACT_NEAR"
mk_sub "$REDEEMER_ID" "$MOCK_NEAR"
mk_sub "$ORACLE_ID" "$MOCK_NEAR"
for i in $(seq 1 "$BUYERS"); do mk_sub "buyer$i.$ROOT_ID" "$BUYER_NEAR"; done

# 3. Contrats
deploy() { # deploy <compte> <wasm> <args new>
  if [ "$(code_hash "$1")" != "11111111111111111111111111111111" ]; then echo "$1 déjà déployé"; return; fi
  log "Déploiement de $1"
  near contract deploy "$1" use-file "$2" with-init-call new json-args "$3" \
    prepaid-gas '100 Tgas' attached-deposit '0 NEAR' "${SIGN[@]}" 2>&1 | grep -E "Transaction ID|rror" || true
}
deploy "$CONTRACT_ID" "$WASM" "{\"owner_id\":\"$ROOT_ID\",\"redeemer_id\":\"$REDEEMER_ID\",\"reveal_steps\":$REVEAL_STEPS,\"retry_delay_blocks\":$RETRY_DELAY_BLOCKS,\"oracle_delay_blocks\":$ORACLE_DELAY_BLOCKS}"
deploy "$REDEEMER_ID" "$WASM_REDEEMER" "{\"memaster\":\"$CONTRACT_ID\"}"
deploy "$ORACLE_ID" "$WASM_ORACLE" "{\"memaster\":\"$CONTRACT_ID\",\"operator\":\"$ROOT_ID\"}"
view "$CONTRACT_ID" get_config | python3 -m json.tool

# 4. Oracle de prix en deux temps (propose, attendre oracle_delay_blocks, accept)
CFG=$(view "$CONTRACT_ID" get_config)
if [ "$(echo "$CFG" | jget 'd["price_oracle_id"]')" != "$ORACLE_ID" ]; then
  if [ "$(echo "$CFG" | jget '(d["price_oracle_pending"] or {}).get("price_oracle_id")')" != "$ORACLE_ID" ]; then
    log "propose_price_oracle($ORACLE_ID)"
    call "$ROOT_ID" propose_price_oracle "{\"price_oracle_id\":\"$ORACLE_ID\"}" 30 0
    CFG=$(view "$CONTRACT_ID" get_config)
  fi
  FROM=$(echo "$CFG" | jget 'd["price_oracle_pending"]["effective_from"]')
  log "Attente du bloc $FROM pour accept_price_oracle"
  while :; do
    H=$(curl -s "$RPC_URL" -H 'content-type: application/json' \
      -d '{"jsonrpc":"2.0","id":1,"method":"block","params":{"finality":"final"}}' | jget 'd["result"]["header"]["height"]')
    [ "$H" -ge "$FROM" ] && break
    sleep 5
  done
  call "$ROOT_ID" accept_price_oracle '{}' 30 0
fi

# 5. Série v2 à mécaniques (par lots, dépôts du manifeste)
SLUG=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['slug'])" "$SERIES_PARAMS")
OUT=${SERIES_OUT:-$CONTRACT_DIR/scripts/out/$SLUG}
BUILD_ARGS=(--series-id 0 --out "$OUT")
[ -n "${TABLES_VALEUR:-}" ] && BUILD_ARGS+=(--tables-valeur "$TABLES_VALEUR")
NSER=$(view "$CONTRACT_ID" get_series_count)
if [ "$NSER" = 0 ]; then
  log "Série $SLUG : build_series.py"
  python3 "$HERE/build_series.py" "$SERIES_PARAMS" "${BUILD_ARGS[@]}"
  for f in $(python3 -c "import json,sys; print(' '.join(json.load(open(sys.argv[1]))['calls']))" "$OUT/manifest.json"); do
    dep=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['deposits'][sys.argv[2]])" "$OUT/manifest.json" "$f")
    m=${f%%.*}
    [ "$m" = open_series ] && continue
    log "$m ($f, dépôt $dep yocto)"
    call "$ROOT_ID" "$m" "@$OUT/$f" 300 "$dep"
  done
fi
if [ "$(view "$CONTRACT_ID" get_series '{"series_id":0}' | jget 'd["status"]')" = draft ]; then
  log "open_series(0)"
  call "$ROOT_ID" open_series "@$OUT/open_series.json" 300 0
fi
echo "Hash attendu : $(cat "$OUT/table_hash.txt")"
view "$CONTRACT_ID" get_series_table_hash '{"series_id":0}'

# 6. Série de contrôle sans mécanique (create_series, une transaction ; une commune adossée pour le burn)
if [ "${SKIP_CONTROL:-0}" != 1 ]; then
  if [ "$(view "$CONTRACT_ID" get_series_count)" -lt 2 ]; then
    log "Série de contrôle (id 1)"
    CTRL='{"table":{"name":"Controle sans mecanique","price":"50000000000000000000000","cards_per_pack":3,
"rarity_weights":{"mythic":0,"legendary":0,"epic":500,"rare":2500,"common":7000},
"cards":[
{"card_id":"ctrl-com-a","title":"Controle commune A","rarity":"common","weight":1,"cap":null,"media":null,"reference":null,"backing":{"asset_id":"nep141:factice-ctrl.testnet","amount":"1000"}},
{"card_id":"ctrl-com-b","title":"Controle commune B","rarity":"common","weight":1,"cap":null,"media":null,"reference":null,"backing":null},
{"card_id":"ctrl-rare-a","title":"Controle rare A","rarity":"rare","weight":1,"cap":null,"media":null,"reference":null,"backing":null},
{"card_id":"ctrl-epic-a","title":"Controle epique A","rarity":"epic","weight":1,"cap":5,"media":null,"reference":null,"backing":null}],
"mythics":[],"royalties":[{"account_id":"'"$ROOT_ID"'","bps":500}]}}'
    call "$ROOT_ID" create_series "$CTRL" 300 0
  fi
  if [ "$(view "$CONTRACT_ID" get_series '{"series_id":1}' | jget 'd["status"]')" = draft ]; then
    call "$ROOT_ID" open_series '{"series_id":1}' 300 0
  fi
fi

log "État"
for s in 0 1; do view "$CONTRACT_ID" get_series "{\"series_id\":$s}" | python3 -c "
import json,sys; d=json.load(sys.stdin)
if d: print({k: d[k] for k in ('series_id','status','name','table_hash','required_deposit','min_gas','storage_per_pack','packs_sold','card_count')})"; done
echo "Explorer : https://testnet.nearblocks.io/address/$CONTRACT_ID"
