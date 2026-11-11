# Memaster : quelle source de prix pour la résurrection ?

Date : 11/11/2026. Recherche documentaire, sans code.

## En bref

- GMGN n'est pas un bon oracle. Son API existe, mais elle est jeune et peu documentée. Elle est pensée pour le trading, et ses conditions d'usage sont floues.
- Il n'existe aucun oracle décentralisé sur NEAR pour les memecoins morts. Il faut un oracle maison.
- Pour la démo : un bot hors chaîne lit GeckoTerminal et DexScreener, applique des règles simples, signe `set_resurrected` et publie ses preuves.
- Pour une version sérieuse : la même logique, exécutée dans un TEE via OutLayer (NEAR), avec un délai de contestation.

## 1. GMGN : il y a une API, mais pas pour un oracle

- **Accès.** Une « Agent API / OpenAPI » existe (`openapi.gmgn.ai`). On génère une paire de clés Ed25519, puis on dépose la clé publique sur gmgn.ai/ai pour obtenir une clé. Une clé de démo publique existe, en lecture seule et « pour test uniquement ».
- **Chaînes.** Solana, BSC, Base et Ethereum, plus Robinhood chain.
- **Données.** Infos du jeton (prix, volume, capitalisation), pools, chandeliers (1 min à 1 jour), portefeuilles, smart money. Le swap demande en plus une clé de signature et une IP en liste blanche.
- **Limites.** Elles ne sont pas publiées officiellement. Des intégrations tierces décrivent un « leaky bucket » à 20 unités (les chandeliers coûtent 2) et des bannissements temporaires, jusqu'à 5 min. Avant cette API, l'accès passait par une liste blanche d'IP réservée aux traders actifs (source : Mobula, un concurrent).
- **Conditions d'usage.** Je n'ai trouvé aucune CGU d'API publique, et gmgn.ai renvoie 403 aux robots. L'usage pour un oracle automatisé n'est donc ni autorisé ni interdit explicitement. Les scrapers tiers renvoient la responsabilité à l'utilisateur.
- **Verdict.** On peut s'en servir en source d'appoint ou pour l'interface. Pas comme source unique d'un oracle.

## 2. Alternatives multi-chaînes

| Source | Accès gratuit | Historique | Chaînes | Jetons morts |
|---|---|---|---|---|
| **DexScreener** | Sans clé. 300 req/min sur pairs et tokens (60 sur le reste). Usage commercial autorisé, sauf produit concurrent. | Non : prix courant, liquidité, FDV, variations 5 min / 1 h / 6 h / 24 h | Toutes les grandes chaînes | Oui, tant que le pool existe. La liquidité et `pairCreatedAt` sont fournies. |
| **GeckoTerminal** (CoinGecko onchain) | Sans clé, 30 req/min par IP. Plans payants plus généreux. | Oui : OHLCV par pool (`limit` jusqu'à 1000, pagination `before_timestamp`) | Plus de 200 réseaux, 39 M de jetons | Oui au niveau du pool, mais les bougies sont creuses s'il n'y a pas d'échanges |
| **CoinGecko** (agrégé) | Clé Demo gratuite, limitée | Oui | Multi | Mauvais : les jetons inactifs sont souvent retirés ou figés |
| **Birdeye** | Offre gratuite réduite, le reste payant (CU) | Oui | Solana, ETH, BSC, Base, Arbitrum, etc. | Bonne longue traîne, mais l'intérêt vient surtout des offres payantes |
| **Jupiter Price v3** | 0,5 req/s sans clé, 1 req/s avec clé gratuite | Non | Solana seulement | **Non** : un jeton sans échange depuis 7 jours, ou signalé par les heuristiques, est absent de la réponse |
| **DefiLlama coins** | Sans clé (`coins.llama.fi`) | Oui : historique, graphiques, `searchWidth` | Multi (`chain:adresse`) | Partiel. Le champ `confidence` aide à écarter les prix douteux. |

**Duo recommandé : GeckoTerminal + DexScreener.** Ils sont indépendants, gratuits, multi-chaînes et indexent les pools morts. GeckoTerminal fournit l'historique pour la moyenne sur N jours. DexScreener fournit la liquidité et sert de contrôle croisé du prix courant. DexScreener n'ayant pas d'historique, le bot doit garder ses propres instantanés.

## 3. Oracles décentralisés sur NEAR : non, confirmé

- **Pyth.** `pyth-oracle.near` figure dans la doc NEAR. La doc Pyth indique pourtant que « Pyth Core ne supporte plus NEAR ». Il faut vérifier avant tout usage. De toute façon, Pyth ne couvre que des flux listés : quelques gros memecoins vivants, jamais des jetons morts.
- **Chainlink.** Il y a eu une annonce en 2020 et une subvention d'intégration, mais je n'ai trouvé aucun flux actif sur NEAR en 2026. La doc NEAR des oracles ne le cite pas.
- **Flux.** Il est devenu First Party Oracle (`fpo-node`) et n'est plus mis en avant sur NEAR. Il ne couvre pas la longue traîne.
- **`priceoracle.near` (NearDefi/Burrow).** Il ne fournit que les actifs des protocoles de prêt.
- **OutLayer `price-oracle.near`.** C'est un oracle sécurisé par TEE et compatible Pyth. Surtout, OutLayer exécute du **code WASM personnalisé** avec une attestation TEE, appelable depuis un contrat NEAR (yield/resume). C'est la vraie piste « sérieuse ».

Conclusion : aucun flux prêt à l'emploi ne couvre un memecoin mort. Le rôle `price_oracle` abstrait est le bon choix.

## 4. Règles anti-manipulation

Ordre de grandeur. Dans un pool AMM x·y=k, multiplier le prix par *m* exige d'ajouter environ (√m − 1) fois la réserve en stable. Prenons un pool mort avec 5 k$ de liquidité, donc 2,5 k$ par côté. Un ×10 coûte environ 2,5 k$ × 2,16, soit **5,4 k$**. Avec 100 k$ de liquidité, le même ×10 coûte environ 108 k$, et ce capital reste exposé pendant toute la fenêtre.

Règles proposées, à cumuler :

1. **Seuil relatif au pic.** Le prix doit dépasser X % du plus haut historique (par exemple 10 %) **et** valoir au moins ×10 le plancher de « mort ». Le seuil est figé dans le contrat à la création de la carte.
2. **Durée, pas moyenne seule.** Il faut une médiane journalière (ou un TWAP) au-dessus du seuil **chaque jour** pendant N = 7 jours. Une moyenne simple se fait tirer par un seul pic.
3. **Liquidité minimale.** Exiger au moins 100 k$ sur le pool principal pendant toute la fenêtre. Ajouter un volume 24 h d'au moins 25 k$ et un nombre minimal d'acheteurs distincts (GMGN ou Birdeye peuvent le fournir).
4. **Pool éligible.** Écarter les pools créés pendant la fenêtre (`pairCreatedAt`) et ceux qui se cotent contre un jeton exotique. Ne garder que les paires USDC, USDT ou jeton natif.
5. **Sources concordantes.** Au moins 2 sources indépendantes, avec un écart maximal de 5 % sur le prix et la liquidité. Un désaccord ou une source muette suffit à refuser.
6. **Délai de contestation.** `set_resurrected` crée d'abord un état « en attente » pendant 48 à 72 h. Un compte gardien (multisig de l'équipe) peut opposer un veto. Après ce délai, l'état est finalisé et le brûlage s'ouvre.
7. **Garde-fous.** Une seule résurrection par jeton et par saison. Les preuves (instantanés JSON et leur hash) sont publiées avec l'appel.

## 5. Recommandation

**Démo de hackathon (quelques heures).**
- Prévoir un compte `price_oracle` tenu par un bot Node ou Python hors chaîne.
- Le bot lit GeckoTerminal (OHLCV journalier sur 7 jours) et DexScreener (prix et liquidité du moment). Il applique les règles 1 à 5 avec des seuils abaissés.
- Il signe `set_resurrected(token, preuve_hash)` et publie la preuve : JSON des réponses, horodatage, URLs, dans un gist, sur IPFS ou dans un événement.
- Ajouter un mode « forcer » pour la démo en direct, clairement étiqueté. Le jury doit voir la règle et la preuve, pas seulement le résultat.

**Version sérieuse.**
- Garder le même code de règles, compilé en WASM et exécuté sur **OutLayer (TEE)**. Le contrat n'accepte que les résultats attestés : on n'a plus de clé de bot à protéger ni à croire sur parole.
- En complément ou en option, lire directement l'état des pools sur chaque chaîne via RPC (TWAP Uniswap v3 `observe()`, réserves Raydium) plutôt que des API web. Cela supprime la dépendance aux CGU et aux limites de débit.
- Ajouter un délai de contestation, un veto multisig et une 3e source (Birdeye payant ou DefiLlama).
- NEAR Chain Signatures ne sert pas ici : cet outil sert à *signer* sur d'autres chaînes, pas à *lire* un prix. Il ne deviendrait utile que si la résurrection devait déclencher une action sur Solana ou sur une chaîne EVM.

## Sources

- GMGN CLI (officiel npm) : https://cdn.jsdelivr.net/npm/gmgn-cli@1.5.2/Readme.md
- GMGN : skill marché (limites, kline) : https://skills.cat/skills/gmgnai/gmgn-skills/gmgn-market
- GMGN : accès fermé selon Mobula : https://docs.mobula.io/guides/gmgn-closed-apis
- GMGN : flux de clé via dltHub : https://dlthub.com/context/source/gmgn-api
- DexScreener API : https://docs.dexscreener.com/api/reference
- DexScreener CGU API : https://docs.dexscreener.com/api/api-terms-and-conditions
- GeckoTerminal FAQ (30 req/min) : https://apiguide.geckoterminal.com/faq
- CoinGecko onchain OHLCV : https://docs.coingecko.com/reference/pool-ohlcv-contract-address
- CoinGecko API sans clé : https://docs.coingecko.com/docs/keyless-public-api
- Birdeye limites : https://docs.birdeye.so/docs/rate-limiting
- Birdeye réseaux : https://docs.birdeye.so/docs/supported-networks
- Jupiter Price API v3 : https://developers.jup.ag/docs/price
- DefiLlama API : https://api-docs.defillama.com/
- Oracles NEAR (Pyth, OutLayer) : https://docs.near.org/primitives/oracles
- Pyth et NEAR : https://docs.pyth.network/price-feeds/contract-addresses/near
- OutLayer : https://docs.near.org/primitives/off-chain-compute/outlayer
- Chainlink sur NEAR (2020) : https://pages.near.org/?p=4587
- Flux FPO : https://github.com/fluxprotocol/fpo-node
