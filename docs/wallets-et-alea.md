# Boosters de memecoins sur NEAR : wallets, aléa, taux publics, NFT

Recherche du 10 novembre 2026. Projet étudié : des boosters vendus en NEAR, des cartes NFT NEP-171 revendables, des
taux de tirage publics sur la chaîne, et un burn qui rend des tokens. MetaMask est le wallet principal voulu.

**Méthode et limite.** Tout vient de résultats de recherche web (extraits et résumés de pages). Aucune page n'a été
lue en entier, aucun contrat déployé, aucun appel réel avec MetaMask. « Vérifié » veut donc dire « dit par une source
de référence dans les extraits », pas « testé par nous ».

| Marque | Sens |
| --- | --- |
| **[V]** | Vérifié : source officielle ou spécification |
| **[P]** | Partiel : source secondaire, ancienne, ou sources en désaccord |
| **[NV]** | Non vérifié : rien trouvé, ou souvenir non confirmé |
| **[A]** | Analyse de notre part, déduite des faits ci-dessus |

## En bref

- MetaMask ne gère pas NEAR nativement. La voie conseillée : un compte NEAR `0x…` (eth-implicit), piloté par MetaMask
  via near-connect.
- Cette voie permet tout le produit (achat, transfert, mise en vente, burn), mais une seule action par signature, et
  son état réel sur mainnet reste à tester en premier.
- Aléa : acheter en une transaction, puis tirer dans des callbacks internes sur plusieurs blocs. L'acheteur n'a alors
  plus aucune prise sur le résultat.
- Taux fixes avec plafonds par carte, plutôt qu'un paquet fini de cartes : attendre le « bon moment » ne rapporte rien.
- Marché intégré au contrat des cartes : aucune place de marché NEAR n'a pu être confirmée active.

## 1. MetaMask et NEAR

### Ce que MetaMask gère nativement

| Réseau | Statut | Détail |
| --- | --- | --- |
| Ethereum, Base | **[V]** | Réseaux EVM listés par MetaMask ([annonce](https://metamask.io/news/multichain-accounts)) |
| Solana | **[V]** | Natif : chaque compte a une adresse Solana à côté de l'adresse EVM ([support](https://support.metamask.io/configure/networks/navigating-solana/)). Pas sur les comptes matériels ([support](https://support.metamask.io/configure/accounts/multichain-accounts/)) |
| Monad | **[P]** | Annoncé « bientôt », puis listé comme pris en charge sur des pages plus récentes ([guide](https://metamask.io/news/best-mobile-crypto-wallets-2026), [carte](https://support.metamask.io/trade/metamask-card/funding/)). Pas de note de version datée trouvée |
| NEAR | **Non natif [P]** | Un guide de juin 2026 cite Solana, Bitcoin et Tron comme natifs, pas NEAR ([Datawallet](https://www.datawallet.com/crypto/add-near-to-metamask)). Aucune annonce contraire trouvée |

Les comptes multichaînes associent une adresse EVM, une Solana et une Bitcoin (Extension 13.5, Mobile 7.57,
[MetaMask](https://metamask.io/news/metamask-vs-phantom-vs-rabby)).

### Les trois façons d'utiliser NEAR avec MetaMask

**A. Comptes eth-implicit (NEP-518), recommandé.** Le compte NEAR porte le nom `0x…` de l'adresse Ethereum. MetaMask
signe, un relais transmet, et un contrat de portefeuille vérifie la signature puis exécute l'action NEAR. Les fonds
restent sur NEAR ([evm-on-near](https://evm-on-near.dev/how-it-works/)).

**B. NEAR Snap.** Crée un vrai compte NEAR dans MetaMask ([NEAR](https://medium.com/nearprotocol/metamask-is-now-usable-on-near-via-near-snap-586e7e5e8be9)).
Écarté comme voie principale : Snap tiers à installer, non garanti par MetaMask
([FAQ](https://support.metamask.io/configure/snaps/metamask-snaps-faq/)), et son équipe se serait tournée vers HOT
Wallet selon une source secondaire. État 2026 **[NV]**.

**C. Aurora.** Un réseau EVM séparé : des cartes créées là ne seraient pas des NFT NEP-171. Hors sujet ici **[A]**.

near-connect est le connecteur recommandé à la place de wallet-selector
([dépôt](https://github.com/near/wallet-selector)). Ce n'est pas un wallet : il charge l'adaptateur Ethereum par
manifeste ([docs](https://docs.near.org/web3-apps/tutorials/wallet-login)).

### Ce qu'un utilisateur MetaMask peut faire avec un compte `0x…`

| Capacité | Réponse | Statut |
| --- | --- | --- |
| Transfert de NEAR | Oui | **[V]** [NEP-518](https://github.com/near/NEPs/blob/master/neps/nep-0518.md) |
| Appel de contrat | Oui, via `functionCall(string,string,bytes,uint64,uint32)` | **[V]** NEP-518 |
| Dépôt attaché | Oui. Montant = valeur Ethereum × 1e6 + reste en yocto (champ `uint32` < 1 000 000). Plafond pratique : la valeur doit tenir dans un u128 après multiplication | **[V]** NEP-518 |
| `nft_transfer` et son yoctoNEAR obligatoire | Oui, c'est un appel de contrat ordinaire. ERC-721 n'est pas émulé (travail futur) | **[A]** d'après NEP-518, à tester |
| Plusieurs actions d'un coup | **Non** : une action par transaction, les lots partent l'un après l'autre et peuvent rester à moitié faits | **[P]** [eth-wallet](https://github.com/gagdiez/eth-wallet), [Aurora](https://www.npmjs.com/package/@aurora-is-near/ethereum-wallets) |
| Gaz maximal | 270 Tgas par l'adaptateur, 300 côté relais | **[P]** eth-wallet |
| Signature NEP-413, actions déléguées, clé de connexion | **Non** avec cet adaptateur. Chaque action demande donc une approbation | **[P]** eth-wallet |
| Clé d'accès complet | **Non**, bloquée par le contrat | **[V]** NEP-518 |
| Gaz payé par | Le solde NEAR du compte `0x…` : il faut donc l'alimenter | **[P]** NEP-518, eth-wallet |

**Conséquences pour le produit [A].**

- Acheter un booster, stockage inclus, doit tenir en un seul appel : prix et stockage dans le même dépôt.
- Toujours identifier l'utilisateur par `predecessor_account_id`, comme le conseille la
  [checklist NEAR](https://docs.near.org/smart-contracts/security/checklist).
- Il faut alimenter le `0x…` en NEAR : 1Click sait livrer sur une destination donnée
  ([docs](https://docs.near-intents.org/integration/distribution-channels/1click-api/quickstart/making-a-request)),
  mais recevoir du NEAR natif (et non wNEAR) sur un `0x…` est **[NV]**.

**Attention, signaux contradictoires sur l'état réel :**

- une [modification de la doc NEAR d'octobre 2026](https://github.com/near/docs/pull/3130) retire la section Ethereum
  Wallets du guide de connexion, et demande elle-même si la voie est toujours valable ;
- le README d'eth-wallet indique que le test réel sur mainnet reste à faire ;
- à l'inverse, un [ticket d'un projet tiers](https://github.com/vinibarbosabr/thecoding-app/issues/14) dit l'avoir
  vérifié sur mainnet le 9 octobre 2026.

C'est le **premier point à tester**.

### Faire arriver des tokens sur une adresse Solana après connexion en EVM

L'adresse Solana n'est pas déductible de l'adresse EVM. MetaMask la détient, mais le site doit la demander : session
multichaîne avec le scope `solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp`
([docs](https://docs.metamask.io/metamask-connect/multichain/concepts/sessions/)). Cela s'ajoute a priori à la
connexion near-connect **[A]**, à tester. Pour les comptes matériels, saisie manuelle obligatoire.

Le burn prend l'adresse en argument : `redeem(token_id, chaine, adresse)`. La signature du compte `0x…` suffit à
autoriser l'envoi. Une erreur d'adresse serait irréversible : valider le format sur la chaîne (base58, 32 octets) et
faire confirmer à l'écran **[A]**.

| Voie | Pour | Contre | Statut |
| --- | --- | --- | --- |
| **Omni Bridge** depuis le contrat (`ft_transfer_call`, destinataire `sol:…`) | Pas de serveur, Solana et Base couverts | Le token doit exister en NEP-141. Frais séparés. Lancement par un contrat non confirmé | **[P]** [Omni](https://github.com/Near-One/omni-bridge), [SDK](https://github.com/Near-One/bridge-sdk-js) |
| **NEAR Intents / 1Click** | Solana, Base, Monad, Ethereum listés ([chaînes](https://docs.near-intents.org/resources/chain-support)) | Demande un service pour les cotations. Retrait direct par contrat **[NV]**. Pas de testnet | **[P]** |
| **Chain Signatures** : coffre Solana contrôlé par le contrat | SPL natif, sans pont | Plus de code, un relais pour publier | **[V]** principe ([docs](https://docs.near.org/chain-abstraction/chain-signatures/implementation)) |

Sur Ethereum, Base et Monad, l'adresse de réception est le même `0x…` **[A]**. Monad passe par le pont HOT et non Omni
([docs](https://docs.near-intents.org/integration/bridging/overview)).

La disponibilité de chaque memecoin est à contrôler sur l'API 1Click, seule liste à jour
([docs](https://docs.near-intents.org/resources/asset-support)).

## 2. Aléa équitable

### Ce que garantit `env::random_seed`

- La graine vient du validateur qui produit le bloc : il signe le hash du bloc précédent. Elle est déterministe et
  vérifiable **[V]** ([docs](https://docs.near.org/smart-contracts/security/random)).
- Seul ce validateur la connaît à l'avance, et il ne peut pas la modifier. Il peut en revanche décider d'inclure une
  transaction seulement si le résultat l'arrange **[V]** (même page).
- Elle ne change pas d'un appel à l'autre dans la même méthode ou le même bloc **[V]**
  ([near-sdk](https://docs.rs/near-sdk/latest/near_sdk/env/fn.random_seed.html)).
- Elle serait aussi mélangée à l'identifiant de chaque action dans nearcore : **[NV]**, souvenir non confirmé. Il faut
  donc toujours mélanger soi-même `pack_id` et compte, pour que deux boosters du même bloc ne tirent pas pareil **[A]**.

### Qui peut prédire ou biaiser

| Acteur | Peut prédire | Peut biaiser | Statut |
| --- | --- | --- | --- |
| Utilisateur normal | Non, pour un bloc futur | Seulement s'il peut annuler ou rejouer (voir ci-dessous) | **[A]** |
| Producteur du bloc | Oui, pour son bloc | Par sélection ou rétention, pas par modification | **[V]** |
| Équipe du projet | Non, sauf graine secrète ou contrat modifiable | Oui si le contrat reste modifiable | **[A]** |
| Oracle externe | Dépend de son modèle | Dépend de son modèle | Voir VRF |

**Exploits connus.** Aucun exploit documenté de booster sur NEAR trouvé **[NV]**. Le risque est décrit par la doc
NEAR, et l'annulation après résultat est une attaque connue ailleurs
([article, attribution probable d'après les extraits](https://compass.sustech.edu.cn/paper/bftrand-dsn24.pdf)) **[P]**.

### Simuler l'ouverture et annuler : ce qui marche et ce qui ne marche pas

Sur NEAR, on ne peut pas revenir en arrière d'un reçu à l'autre : un échec plus loin laisse les reçus précédents
validés ([cycle de vie](https://docs.near.org/protocol/transactions/transaction-execution)) **[V]**. Le schéma
classique sur Ethereum (ouvrir dans un contrat, regarder, tout annuler) ne s'applique donc pas directement.

Une simulation en lecture ne donne pas la graine d'un bloc futur **[A]**. Restent quatre failles, à fermer **[A]** :

1. **Tirage dans le même reçu que le paiement.** Un producteur de bloc peut alors viser le résultat.
2. **Relance après échec.** Si le tirage échoue faute de gaz sur certains résultats (une carte rare coûte plus de
   stockage), l'attaquant filtre et relance avec une nouvelle graine. Il faut un gaz fixé par le contrat, et du
   stockage prépayé pour le pire cas.
3. **Remboursement par notification.** Livrer la carte ou prendre le paiement via `nft_transfer_call` ou
   `ft_transfer_call` permet au contrat receveur de refuser. Ce mécanisme ressemble à la faille de NEAR Intents
   d'octobre 2026 (3,8 M$) : une notification volontairement mise en échec a provoqué un remboursement, alors que le
   crédit restait acquis ([résumé](https://www.kucoin.com/news/flash/near-intents-releases-post-mortem-report-on-3-8m-vulnerability)) **[P]**.
4. **Annulation prévue par le contrat.** Pas de fonction d'annulation ou de remboursement une fois le booster payé.

### Commit-reveal en deux transactions, ou tirage en callbacks

La doc NEAR recommande le commit-reveal pour les jeux ([front-running](https://docs.near.org/smart-contracts/security/frontrunning)),
et note qu'il reste une part de vulnérabilité **[V]**. Sa page sur l'aléa le mentionne selon certains extraits, pas
selon d'autres **[P]**.

| | Deux transactions | Callbacks internes (recommandé) |
| --- | --- | --- |
| Signatures MetaMask | 2, avec un moment choisi par l'utilisateur | **1** |
| Gaz du tirage | Choisi par l'appelant, à contrôler | Fixé par le contrat |
| Fonds bloqués si l'utilisateur disparaît | Oui, sauf dévoilement par un tiers | Non |
| Délai entre blocs | `block_height` > bloc d'achat à vérifier | Natif : un reçu par bloc environ |

Le callback s'exécute dans un bloc différent, en général 1 à 2 blocs plus tard
([docs](https://docs.near.org/smart-contracts/anatomy/crosscontract)) **[V]**. Qu'un appel d'un contrat à lui-même
suive le même rythme est une déduction **[A]**, à mesurer sur testnet.

### Options de VRF

- **OutLayer VRF.** Sortie accompagnée d'une preuve : signature Ed25519 sur `vrf:{request_id}:{sender_id}:{seed}`,
  vérifiable dans le contrat pour environ 1 Tgas, résultat renvoyé par yield/resume
  ([docs](https://outlayer.fastnear.com/docs/vrf)) **[V sur le principe, source unique : l'éditeur]**.
  - Confiance reportée sur le matériel Intel TDX et la gouvernance d'OutLayer. La doc NEAR conseille d'évaluer ce
    service avant un usage en production ([docs](https://docs.near.org/primitives/off-chain-compute/outlayer)).
  - Ni audit indépendant ni grille tarifaire trouvés **[NV]**.
  - Une signature Ed25519 n'est pas unique par construction, contrairement à un vrai VRF : un signataire malhonnête
    pourrait en produire plusieurs. La protection repose donc sur le matériel **[A]**.
- **Chainlink VRF, Pyth Entropy, Switchboard sur NEAR.** Aucune trace trouvée **[NV]**.

### Conception anti-snipe recommandée

1. `buy_pack(serie)` : prix et stockage dans le dépôt, gaz minimal exigé, booster enregistré `Pending`, paiement
   définitif.
2. Enchaîner k reçus internes `#[private]` (k = 3 à 5) à gaz fixe. Chacun accumule
   `acc = sha256(acc || random_seed || pack_id || owner)`.
3. Le dernier reçu tire les cartes depuis `acc`, crée les NFT, journalise tout. Il ne doit échouer pour aucun résultat.
4. `retry_reveal(pack_id)`, ouvert à tous, uniquement si le tirage n'a jamais écrit de résultat et après un délai.
5. Livraison par création directe, jamais par `*_transfer_call`.

**Ce que ça change [A].** L'acheteur ne peut ni voir, ni choisir, ni annuler. Un validateur doit contrôler le dernier
bloc de la chaîne pour avoir un avantage, et cet avantage se limite à retenir un bloc, à perte de récompense. Ajouter
OutLayer serait un renfort pour les séries de grande valeur : sa sortie doit être fixée **avant** la dernière graine
de chaîne.

## 3. Taux de tirage publics et vérification

Rien de trouvé sur un booster NEAR déjà en place avec taux vérifiables **[NV]**. Conception proposée **[A]** :

- **Table en état du contrat.** Par série : prix, cartes par booster, et pour chaque carte `poids`, `plafond`, `créées`,
  `quantité de tokens`. Exposée par une fonction de lecture.
- **Figée à l'ouverture** de la série, avec `hash_table` publié. Sinon, la table ne prouve rien.
- **Taux fixes avec plafonds, pas un paquet fini.** Avec un paquet fini, les comptes restants sont publics : un robot
  achète quand il ne reste presque que des cartes rares. Avec des taux fixes, atteindre un plafond fait retomber sur
  la rareté inférieure : la valeur attendue ne fait que baisser, donc attendre ne rapporte rien.
- **Pas de graine secrète de l'équipe.** Un `sha256(graine)` publié d'avance donne à l'équipe la connaissance de la
  graine et un pouvoir de rétention. Inutile avec les callbacks.
- **Contrat non modifiable** pendant la série (clés retirées ou gouvernance à délai), code publié et build reproductible.

**Vérificateur public.** Page ou script qui :

1. lit la table et compare son hash ;
2. compare le hash du code déployé au code publié ;
3. pour chaque événement `pack_revealed {pack_id, owner, seeds, acc, tirages, cartes}`, recalcule le tirage ;
4. compare les fréquences observées aux taux annoncés sur toute la série.

**Limite.** Relier une graine journalisée à la valeur aléatoire d'un bloc public depuis l'extérieur n'est pas
confirmé **[NV]**. La preuve repose donc sur le code déployé, qui journalise la graine reçue de `env::random_seed`.

## 4. NFT, cartes et marché

### Standards

| Standard | Rôle | Statut |
| --- | --- | --- |
| NEP-171 | Cœur. Événement `nft_burn` et version 1.2.0 avec `nft_metadata_update`. Le contrat doit vider les approbations à chaque transfert réussi | **[V]** [NEP-171](https://github.com/near/NEPs/blob/master/neps/nep-0171.md) |
| NEP-177 | Métadonnées (statut Final), `nft_metadata()` et `metadata` par token | **[V]** [NEP-177](https://github.com/near/NEPs/blob/master/neps/nep-0177.md). Détail des champs `reference`, `reference_hash`, `extra`, `copies` : souvenir **[NV]** |
| NEP-178 | Approbations : `nft_approve`, `nft_revoke`, `nft_revoke_all`, `nft_is_approved`, identifiant qui s'incrémente | **[V]** [discussion](https://github.com/near/NEPs/discussions/178), [exemple](https://github.com/near-examples/nft-tutorial/blob/main/nft-contract/src/approval.rs) |
| NEP-199 | Redevances : `nft_payout`, `nft_transfer_payout`, `max_len_payout` | **[P]** texte de la spécification non retrouvé, implémentations tierces seulement |

**Métadonnées dynamiques.** L'événement `nft_metadata_update` prévient les indexeurs **[V]**. Il faut l'émettre si une
carte change.

**Quantité de tokens variable par carte [A].** La valeur fait foi dans l'état du contrat (`token_id → montant`), fixée
au tirage. `extra` ne sert qu'à l'affichage. Le stock doit être réservé au tirage et l'invariant
`coffre ≥ total réservé` vérifié, sinon le dernier à brûler n'est pas payé. La quantité est fixe en tokens, pas en
valeur : avec un memecoin, le prix peut s'effondrer.

### Places de marché actives fin 2026

| Marché | Situation | Statut |
| --- | --- | --- |
| TradePort | Pages de collections NEAR visibles, se présente comme actif sur NEAR. Statistiques non datées | **[P]** seule présence constatée ([site](https://www.tradeport.xyz/)) |
| Mintbase | Classé parmi ceux qui ont quitté les NFT dans une étude d'octobre 2026, recentrage dès 2023. Présence web, activité inconnue | **[P]** ([étude](https://cryptodiffer.com/feed/project-updates/nft-market-2026-marketplaces-survival), [fiche](https://app.coinpedia.org/company/mintbase/)) |
| Paras | Même classement, aucune annonce officielle trouvée | **[P]** |
| Few and Far, tofuNFT, Jump.trade | Cités, sans preuve d'activité 2026. DappRadar affiche 0 $ partout, page probablement figée | **[NV]** ([DappRadar](https://dappradar.com/rankings/nft/marketplaces/chain/near)) |
| Bitte | Rien trouvé | **[NV]** |

**Conclusion : aucun marché NEAR confirmé actif avec du volume réel.** Il ne faut pas faire reposer la revente sur un
marché tiers.

### Une carte en vente qui est brûlée

La norme ne définit pas le burn d'une carte en vente, seulement l'événement **[V]**. Aucune doc trouvée sur ce cas
exact **[NV]**. Ce que l'on sait des marchés :

- Le marché garde l'identifiant d'approbation et doit gérer les ventes périmées
  ([tutoriel](https://docs.near.org/fr/docs/tutorials/contracts/nfts/marketplace)) **[V]**.
- Le remboursement de l'acheteur dépend du contrat de marché : prévu dans
  [certaines implémentations](https://github.com/keydeveloping/nearsea/pull/14), non confirmé pour Paras **[P]**.
- Une annonce périmée reste achetable tant que le marché figure parmi les approuvés
  ([NEP-171](https://github.com/near/NEPs/discussions/171)) **[P]**.

**Règles proposées [A] :**

1. Le burn exige que la carte ne soit pas en vente, ou efface toute approbation au moment du burn.
2. Burn en deux temps, comme le recommande NEAR pour les états dépendant d'un appel externe
   ([docs](https://docs.near.org/smart-contracts/security/callbacks)) : état `Redeeming` (transfert et vente refusés),
   envoi des tokens, puis dans le callback suppression et `nft_burn` en cas de succès, ou retour à l'état normal en
   cas d'échec. Cela empêche de vendre une carte déjà encaissée et de brûler sans recevoir.
3. Vérifier que le callback ne suppose pas un succès du pont : le succès sur NEAR ne prouve pas l'arrivée sur Solana.

## Conception recommandée

1. **Wallet.** near-connect avec l'adaptateur Ethereum : un compte `0x…` piloté par MetaMask. Wallets NEAR natifs
   gardés en second choix, ce qui protège la démo si l'adaptateur faillit.
2. **Un contrat unique cartes + marché.** `list` et `buy` s'exécutent dans le même contrat et le même reçu, sans
   approbation ni course possible avec le burn. NEP-171, 177, 178 et 199 restent exposés pour les marchés externes.
3. **Achat en une signature**, tirage sur 3 à 5 reçus internes à gaz fixe, sans annulation ni `*_transfer_call`.
4. **Taux fixes avec plafonds**, table figée et hachée, événements complets, page de vérification publique.
5. **Burn en deux temps**, stock réservé dès le tirage, adresse de destination passée en argument et validée.
6. **Solana** : adresse lue via la session multichaîne de MetaMask, envoi par Omni Bridge si le token existe en
   NEP-141. Sinon Chain Signatures avec un coffre Solana.
7. **OutLayer VRF** en amélioration ultérieure, mélangé à la graine de chaîne, pas comme source unique.

## Risques ouverts

| Risque | Gravité | Que faire |
| --- | --- | --- |
| Adaptateur MetaMask non confirmé sur mainnet, retiré de la doc NEAR en octobre 2026 | **Élevée** | Tester en premier : connexion, achat avec dépôt, `nft_transfer`, sur mainnet avec petits montants |
| Connexion Solana en plus de near-connect, parcours peut-être lourd | Moyenne | Prototype ; saisie manuelle en secours |
| Alimenter le `0x…` en NEAR, seul moyen de payer gaz et booster | **Élevée** | Tester le parcours depuis Base ou Ethereum |
| Rétention de bloc par un validateur | Faible à ce stade | Accepter et documenter ; VRF pour les séries chères |
| Rythme réel des callbacks internes | Moyenne | Mesurer sur testnet, et le pire cas de gaz (carte la plus chère, 270 Tgas maximum) |
| Disponibilité des memecoins en NEP-141, ponts | **Élevée** | Vérifier sur 1Click ; le pont Solana → NEAR a connu des blocages ([ticket](https://github.com/Near-One/omni-bridge/issues/666)) |
| Pas de testnet pour Intents, faille d'octobre 2026 | Moyenne | Petits montants, plafond par retrait |
| Pas de liquidité externe sur les cartes | Moyenne | Marché intégré, et le dire clairement |
| Cadre légal : tirage au sort payant, memecoins | **Élevée, non étudiée ici** | Avis juridique avant lancement public |
