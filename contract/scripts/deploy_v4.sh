#!/usr/bin/env bash
# Contrat v4 (types de packs) sur testnet, en une commande, depuis contract/ :
#     ./scripts/deploy_v4.sh
# Crée app4/redeemer4/oracle4.memaster-demo-j7xg7z.testnet, déploie le wasm, installe l'oracle,
# puis charge et ouvre les deux séries déjà construites et versionnées (series-v4/, voir build_v4.py) :
#   0 « Moonpacks Classic » + les 9 packs de la boutique (Dog, Cat, Frog, Solana, BNB Chain, Ethereum, OG 1/2/5)
#   1 « Moonpacks Full Moon »
# Relançable : chaque étape déjà faite est sautée. Clés : ~/.near-credentials du compte racine (rien dans le repo).
# Coût : ~11 NEAR (compte du contrat) + ~6,3 NEAR de dépôts de stockage des deux séries + mocks.
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
CONTRACT_DIR=$(dirname "$HERE")
R=${ROOT_ID:-memaster-demo-j7xg7z.testnet}
COMMUN=(ROOT_ID=$R CONTRACT_ID=${CONTRACT_ID:-app4.$R} REDEEMER_ID=${REDEEMER_ID:-redeemer4.$R}
        ORACLE_ID=${ORACLE_ID:-oracle4.$R} CONTRACT_NEAR=${CONTRACT_NEAR:-11} SKIP_CONTROL=1 PREBUILT=1)
# Les mythiques sont celles de app3 (mêmes engagements) : les préimages de app3 servent au contrôle.
S0=$HERE/secrets/serie-demo-entree.json
S1=$HERE/secrets/serie-demo-standard.json
env "${COMMUN[@]}" SERIES_ID=0 SERIES_OUT="$CONTRACT_DIR/series-v4/classic" SECRETS="$S0" "$HERE/deploy_testnet.sh"
env "${COMMUN[@]}" SKIP_BUILD=1 SERIES_ID=1 SERIES_OUT="$CONTRACT_DIR/series-v4/full-moon" SECRETS="$S1" "$HERE/deploy_testnet.sh"
C=${CONTRACT_ID:-app4.$R}
echo
echo "Fini. Pour basculer le site sur $C :"
echo "  gh variable set CONTRACT_ID --body $C && gh workflow run ci.yml --ref main"
