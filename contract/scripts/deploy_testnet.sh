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
#   SERIES_ID            identifiant de la série à charger (défaut 0) : relancer le script avec
#                        SERIES_ID=1 et d'autres SERIES_PARAMS / SERIES_OUT pour une 2e série
#   CATALOGUE            catalogue passé à build_series.py --catalogue (optionnel, ex. ../docs/data/catalogue-demo.json)
#   SELS                 build_series.py --sels (sels existants, ex. scripts/secrets/serie-v2.json ; optionnel)
#   MEDIA_BASE           build_series.py --media-base (ex. ipfs://<CID>/ ; optionnel)
#   SKIP_BUILD=1         ne pas reconstruire les wasm
#   KEYCHAIN             « legacy » (défaut, ~/.near-credentials) ou « system » (trousseau du système, clés
#                        importées avec save-to-keychain) : où lire les clés et ranger celles des sous-comptes
#   SKIP_CONTROL=1       ne pas créer la série de contrôle sans mécanique
#   PREBUILT=1           SERIES_OUT contient déjà les arguments (ex. series-v4/classic, de build_v4.py) :
#                        pas de build_series.py ; SERIES_PARAMS est ignoré
#   SECRETS              préimages des mythiques pour validate_series.py (défaut scripts/secrets/<slug>.json
#                        s'il existe ; sans fichier, la validation se fait sans contrôle des préimages)
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
# Comptes : nom NEAR valide en .testnet (ils servent aussi de chemins dans ~/.near-credentials).
for id in "$ROOT_ID" "$CONTRACT_ID" "$REDEEMER_ID" "$ORACLE_ID"; do
  if ! [[ ${#id} -ge 2 && ${#id} -le 64 && $id =~ ^(([a-z0-9]+[-_])*[a-z0-9]+\.)*([a-z0-9]+[-_])*[a-z0-9]+$ && $id == *.testnet ]]; then
    echo "Refus : compte invalide ou hors testnet : $id" >&2; exit 1
  fi
done
BUYERS=${BUYERS:-3}
CONTRACT_NEAR=${CONTRACT_NEAR:-7}
MOCK_NEAR=${MOCK_NEAR:-1.5}
BUYER_NEAR=${BUYER_NEAR:-3}
REVEAL_STEPS=${REVEAL_STEPS:-3}
RETRY_DELAY_BLOCKS=${RETRY_DELAY_BLOCKS:-100}
ORACLE_DELAY_BLOCKS=${ORACLE_DELAY_BLOCKS:-30}
SERIES_PARAMS=${SERIES_PARAMS:-$HERE/serie-exemple.json}
case "${KEYCHAIN:-legacy}" in
  legacy) SIGN=(network-config testnet sign-with-legacy-keychain send); SAVE_KEY=save-to-legacy-keychain ;;
  system) SIGN=(network-config testnet sign-with-keychain send); SAVE_KEY=save-to-keychain ;;
  *) echo "KEYCHAIN doit valoir legacy ou system" >&2; exit 1 ;;
esac

log() { printf '\n== %s\n' "$*"; }

# Vue JSON par RPC (sortie : le résultat décodé, ou « null » si la vue panique ou le compte n'existe pas).
view() {
  python3 - "$RPC_URL" "$1" "$2" "${3:-}" <<'PY'
import base64, json, sys, time, urllib.request
rpc, acc, meth, args = sys.argv[1:5]
args = args or "{}"  # (bash 3.2 de macOS : "${3:-{\}}" donnait « {\} », qui n'est pas du JSON)
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
# 0 : le compte existe ; 1 : le RPC répond qu'il n'existe pas ; 2 : RPC injoignable ou réponse
# inattendue (après 5 essais). Seul 1 permet de conclure à l'absence.
account_exists() {
  python3 - "$RPC_URL" "$1" <<'PY'
import json, sys, time, urllib.request
rpc, acc = sys.argv[1:3]
body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "query", "params": {
    "request_type": "view_account", "finality": "final", "account_id": acc}}).encode()
for attempt in range(5):
    try:
        r = json.load(urllib.request.urlopen(urllib.request.Request(rpc, body, {"content-type": "application/json"}), timeout=20))
    except Exception:
        time.sleep(2 * (attempt + 1))
        continue
    if "result" in r:
        sys.exit(0)
    if "UNKNOWN_ACCOUNT" in json.dumps(r.get("error", {})):
        sys.exit(1)
    time.sleep(2 * (attempt + 1))
sys.exit(2)
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
call() { # call <signer> <method> <json-args|@fichier> <gaz Tgas> <dépôt yocto> ; s'arrête en cas d'échec
  local signer=$1 method=$2 args=$3 gas=$4 dep=$5 a out rc=0
  if [[ $args == @* ]]; then a=(file-args "${args#@}"); else a=(json-args "$args"); fi
  out=$(near contract call-function as-transaction "$CONTRACT_ID" "$method" "${a[@]}" \
    prepaid-gas "$gas Tgas" attached-deposit "$dep yoctonear" sign-as "$signer" "${SIGN[@]}" 2>&1) || rc=$?
  printf '%s\n' "$out" | grep -E "Transaction ID|rror|panicked|Smart contract" || true
  # Avant, le « || true » du filtre avalait tout échec (panique, dépôt insuffisant) malgré set -e.
  if [ "$rc" -ne 0 ] || printf '%s' "$out" | grep -qE "panicked|Failure|rror"; then
    echo "Échec de $method (code $rc) : arrêt" >&2; exit 1
  fi
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
  local st=0
  account_exists "$1" || st=$?
  if [ "$st" = 0 ]; then echo "$1 existe"; return; fi
  [ "$st" = 1 ] || { echo "RPC injoignable : existence de $1 inconnue, arrêt" >&2; exit 1; }
  for attempt in 1 2 3; do
    log "Création de $1 ($2 NEAR), essai $attempt"
    near account create-account fund-myself "$1" "$2 NEAR" autogenerate-new-keypair "$SAVE_KEY" \
      sign-as "$ROOT_ID" "${SIGN[@]}" 2>&1 | grep -E "Transaction ID|created successfully|rror" || true
    sleep 3
    st=0
    account_exists "$1" || st=$?
    [ "$st" = 0 ] && return
    # Ne jamais effacer une clé sans réponse « compte inconnu » du RPC : une erreur réseau juste
    # après une création réussie effacerait la clé d'un compte créé et approvisionné.
    [ "$st" = 1 ] || { echo "RPC injoignable après la création de $1 : clé locale gardée, arrêt" >&2; exit 1; }
    # Échec (vu sur testnet : « Transaction has expired ») : la clé locale générée ne sert à rien.
    rm -rf "$HOME/.near-credentials/testnet/$1" "$HOME/.near-credentials/testnet/$1.json"
    sleep $((attempt * 5))
  done
  echo "Création de $1 impossible" >&2; exit 1
}
mk_sub "$CONTRACT_ID" "$CONTRACT_NEAR"
mk_sub "$REDEEMER_ID" "$MOCK_NEAR"
mk_sub "$ORACLE_ID" "$MOCK_NEAR"
for ((i = 1; i <= BUYERS; i++)); do mk_sub "buyer$i.$ROOT_ID" "$BUYER_NEAR"; done

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

# 5. Série à mécaniques n° SERIES_ID (par lots, dépôts du manifeste)
SERIES_ID=${SERIES_ID:-0}
if [ "${PREBUILT:-0}" = 1 ]; then
  : "${SERIES_OUT:?SERIES_OUT requis avec PREBUILT=1}"
  [ -f "$SERIES_OUT/manifest.json" ] || { echo "$SERIES_OUT/manifest.json absent" >&2; exit 1; }
  OUT=$SERIES_OUT
  SLUG=$(basename "$OUT")
else
  SLUG=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['slug'])" "$SERIES_PARAMS")
  OUT=${SERIES_OUT:-$CONTRACT_DIR/scripts/out/$SLUG}
fi
SECRETS=${SECRETS:-$HERE/secrets/$SLUG.json}
VALIDATE=(python3 "$HERE/validate_series.py" "$OUT")
[ -f "$SECRETS" ] && VALIDATE+=(--secrets "$SECRETS")
BUILD_ARGS=(--series-id "$SERIES_ID" --out "$OUT")
[ -n "${TABLES_VALEUR:-}" ] && BUILD_ARGS+=(--tables-valeur "$TABLES_VALEUR")
[ -n "${CATALOGUE:-}" ] && BUILD_ARGS+=(--catalogue "$CATALOGUE")
[ -n "${SELS:-}" ] && BUILD_ARGS+=(--sels "$SELS")
[ -n "${MEDIA_BASE:-}" ] && BUILD_ARGS+=(--media-base "$MEDIA_BASE")
NSER=$(view "$CONTRACT_ID" get_series_count)
if [ "$NSER" -lt "$SERIES_ID" ]; then
  echo "Série $SERIES_ID demandée, mais seulement $NSER série(s) sur le contrat : charger d'abord les précédentes" >&2; exit 1
fi
if [ "$NSER" = "$SERIES_ID" ]; then
  if [ "${PREBUILT:-0}" = 1 ]; then
    log "Série $SLUG (id $SERIES_ID) : arguments déjà construits dans $OUT"
  else
    log "Série $SLUG (id $SERIES_ID) : build_series.py"
    python3 "$HERE/build_series.py" "$SERIES_PARAMS" "${BUILD_ARGS[@]}"
  fi
  "${VALIDATE[@]}"
  for f in $(python3 -c "import json,sys; print(' '.join(json.load(open(sys.argv[1]))['calls']))" "$OUT/manifest.json"); do
    dep=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['deposits'][sys.argv[2]])" "$OUT/manifest.json" "$f")
    m=${f%%.*}
    [ "$m" = open_series ] && continue
    log "$m ($f, dépôt $dep yocto)"
    call "$ROOT_ID" "$m" "@$OUT/$f" 300 "$dep"
  done
fi
EXPECTED_HASH=$(cat "$OUT/table_hash.txt")
if [ "$(view "$CONTRACT_ID" get_series "{\"series_id\":$SERIES_ID}" | jget 'd["status"]')" = draft ]; then
  # L'ouverture fige la table pour toujours : le brouillon chargé doit être exactement la table
  # locale (nombre de cartes, puis hash recalculé depuis l'en-tête et les pages lus sur la chaîne).
  # Une reprise après un chargement interrompu s'arrête ici au lieu d'ouvrir une table tronquée.
  WANT=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['cards'])" "$OUT/manifest.json")
  HAVE=$(view "$CONTRACT_ID" get_series "{\"series_id\":$SERIES_ID}" | jget 'd["card_count"]')
  if [ "$HAVE" != "$WANT" ]; then
    echo "Brouillon incomplet : $HAVE cartes sur la chaîne, $WANT attendues. Pas d'ouverture." >&2
    echo "Compléter avec append_series_cards (lots manquants de $OUT) ou delete_draft, puis relancer." >&2
    exit 1
  fi
  # La table locale est revalidée juste avant l'ouverture (y compris à la reprise, sans rebuild).
  "${VALIDATE[@]}" \
    || { echo "Table locale refusée par validate_series.py : pas d'ouverture" >&2; exit 1; }
  (cd "$CONTRACT_DIR/../verifier" && python3 -m memaster_verifier table --rpc "$RPC_URL" --contract "$CONTRACT_ID" \
    --series "$SERIES_ID" --draft --expected-hash "$EXPECTED_HASH") \
    || { echo "Brouillon on-chain ≠ table locale (hash) : pas d'ouverture" >&2; exit 1; }
  log "open_series($SERIES_ID)"
  call "$ROOT_ID" open_series "@$OUT/open_series.json" 300 0
fi
ONCHAIN_HASH=$(view "$CONTRACT_ID" get_series_table_hash "{\"series_id\":$SERIES_ID}" | jget 'd["stored"]')
echo "Hash attendu : $EXPECTED_HASH"
echo "Hash on-chain : $ONCHAIN_HASH"
[ "$ONCHAIN_HASH" = "$EXPECTED_HASH" ] || { echo "Hash on-chain ≠ hash attendu" >&2; exit 1; }

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
for s in $(seq 0 $(( $(view "$CONTRACT_ID" get_series_count) - 1 ))); do view "$CONTRACT_ID" get_series "{\"series_id\":$s}" | python3 -c "
import json,sys; d=json.load(sys.stdin)
if d: print({k: d[k] for k in ('series_id','status','name','table_hash','required_deposit','min_gas','storage_per_pack','packs_sold','card_count')})"; done
echo "Explorer : https://testnet.nearblocks.io/address/$CONTRACT_ID"
