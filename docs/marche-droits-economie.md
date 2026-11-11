# Boosters de memecoins : marché, droits, cadre légal et économie

Recherche arrêtée au 10 novembre 2026. **Ce document est une orientation, pas un conseil juridique.** Avant toute vente réelle, il faut l'avis d'un avocat en droit des jeux et en droit des crypto-actifs.

**Produit étudié.** L'utilisateur paie en NEAR et ouvre un booster aléatoire de 5 cartes NFT représentant des memecoins, avec des raretés. Il peut revendre ses cartes. Certaines cartes, quelle que soit leur rareté, peuvent être brûlées pour recevoir les jetons achetés et bloqués **à l'ouverture du booster** (décision de l'équipe). Les cartes de coins morts sont de pure collection.

## Comment lire les statuts

| Statut | Sens |
|---|---|
| **[Vérifié]** | Texte officiel, document du projet, ou plusieurs sources sérieuses concordantes |
| **[Partiel]** | Source secondaire unique, source fragile, ou sources qui divergent |
| **[Non vérifié]** | Cherché sans résultat, ou vient de mémoire |
| **[Inférence]** | Raisonnement de l'auteur à partir des faits sourcés |
| **[Illustratif]** | Chiffre inventé pour l'exemple, à recalibrer |

**Limite de méthode.** La recherche repose sur des extraits renvoyés par un moteur de recherche : aucune page n'a été lue en entier, décret compris. « Vérifié » veut donc dire « confirmé sur extraits ». Les calculs de la partie 4 sont analytiques et faits à la main, sans simulation.

---

## En bref

1. **Le marché existe et il est gros**, mais il repose sur des cartes physiques et sur une revente immédiate à la plateforme, pas sur la collection. Aucun produit identique au nôtre n'a été trouvé (ce qui ne prouve pas qu'il n'en existe pas).
2. **Visuels : tout doit être original.** Les logos des autres coins ne sont pas plus sûrs que Pepe et Doge. Aucune licence ni mention CC0 n'a été trouvée pour aucun d'eux. Voir la réponse directe en 2.1.
3. **Droit français : c'est le point le plus dangereux.** Les quatre critères du jeu d'argent interdit semblent réunis. Le régime JONUM ne couvre pas le produit tel quel : il exige un vrai jeu, interdit le rachat par l'émetteur, et plafonne les récompenses en crypto-actifs à 20 % du chiffre d'affaires du jeu.
4. **Économie : l'achat à l'ouverture supprime le risque de stock et le besoin d'oracle**, mais crée trois sujets : le financement des gros tirages (réserve), le front-running, et un risque de « tirage gratuit » si un échec d'achat rembourse le booster.
5. **Pour le hackathon : testnet ou démonstration fermée, sans vente au public.**

---

## 1. Produits existants

### 1.1 Chiffres de marché

| Acteur | Modèle | Chiffres | Statut |
|---|---|---|---|
| Ensemble du gacha on-chain | Boosters numériques de cartes physiques | [284,3 M$ de boosters vendus en juillet 2026](https://www.tradingview.com/news/cointelegraph:4b632ccea094b:0-gambling-on-random-pok-mon-cards-onchain-gagcha-hits-record-high-as-crypto-sinks/). [358,7 M$ de volume sur 30 jours](https://www.kucoin.com/news/insight/NOW/6aec7998bbcb52000745f14a) selon un post de novembre 2026 | **[Partiel]** les outils de suivi divergent |
| Collector Crypt (Solana, jeton CARDS) | Cartes gradées en coffre, gacha, rachat instantané | [635 M$ de revenu brut cumulé, 576 M$ rendus via rachats, 43 M$ net, 6,7 % de rétention](https://research.4pillars.io/en/research/collector-crypt-has-a-margin-problem) au 13 juin 2026. [57,6 % du flux](https://www.kucoin.com/news/insight/NOW/6aec7998bbcb52000745f14a). [Volume marchand brut (dépenses gacha et marché secondaire) de 406,1 M$ au T2 2026](https://blockworks.com/api/investor-report/collector-crypto-token-holder-report-q2-2026/pdf) | **[Partiel]** analyses tierces fondées sur les données Blockworks |
| Courtyard (Polygon) | Cartes en coffre, 1 pour 1, sans jeton | [Dit viser 2 Md$ de ventes annuelles](https://www.gamblinginsider.com/news/193677/digital-trading-card-boom-gambling-questions) (déclaratif). Part de flux tombée de 44,5 % à 24,5 % entre août et novembre 2026 | **[Partiel]** |
| Phygitals (Solana) | Cartes tokenisées | [Plus de 250 M$ de volume](https://financefeeds.com/how-phygitals-is-bringing-real-world-collectibles/), [vitrine sur Fanatics Collect en avril 2026](https://genfinity.io/2026/04/27/phygitals-fanatics-collect-solana-tokenized-trading-cards/) | **[Partiel]** |
| Jupiter Gacha (Solana) | Boosters adossés à Collector Crypt | [Plus de 50 M$ de volume cumulé](https://solanacompass.com/news/jupiter-gacha-crosses-50m-in-total-trading-volume-on-solana). [Documentation publique sur le rachat et l'espérance](https://docs.jup.ag/user-docs/trade/gacha/instant-buyback) | **[Vérifié]** pour les règles, **[Partiel]** pour le volume |
| Secteur | Sites de reconditionnement numérique | [52 sites recensés par Barron's](https://www.gamblinginsider.com/news/193677/digital-trading-card-boom-gambling-questions) | **[Partiel]** cité de seconde main |

### 1.2 Ce qui marche

- **Afficher l'espérance et donner une sortie immédiate.** Chez Jupiter, chaque booster [affiche sa valeur moyenne, et le rachat va de 85 % à 93 % de la valeur assurée, dans une fenêtre de 3 jours](https://docs.jup.ag/user-docs/trade/gacha/instant-buyback). Courtyard [affirme que la valeur moyenne d'un booster égale son prix](https://au.trustpilot.com/review/courtyard.io?page=4) **[Partiel]**. Rarible a annoncé [504,03 $ d'espérance pour un booster à 500 $](https://egamers.io/?p=124197) **[Partiel]**.
- **Les très gros boosters font le volume.** Un booster à 2 500 $ aurait fait [82,9 M$ en trois semaines, environ 40 % du volume de juin](https://www.bit.fan/en/news/list/collector-crypt-trading-card-infrastructure-cards-analysis-ba1b7abe-en-keyName-c975e97c) chez Collector Crypt **[Partiel]**.
- **Tourner vite.** [71,8 % du volume de juin passe par le mode « turbo »](https://research.4pillars.io/en/research/collcector-crypt-has-one-question-left), qui revend aussitôt à la plateforme **[Partiel]**.

### 1.3 Ce qui fragilise ou a échoué

- **Peu de collectionneurs.** Le dirigeant de Collector Crypt dit que [jusqu'à 98 % des cartes ouvertes sont revendues aussitôt](https://www.gamblinginsider.com/news/193677/digital-trading-card-boom-gambling-questions) **[Partiel]**. 4Pillars décrit [une demande concentrée sur l'achat-revente](https://research.4pillars.io/en/research/collector-crypt-distorted-growth-drivers-and-the-absence-of-the-real-card-market). Cela ressemble davantage à du jeu qu'à de la collection, ce qui pèse sur l'analyse juridique **[Inférence]**.
- **Marges minces et sous contrôle de la plateforme.** Valeur assurée et taux de rachat [sont deux réglages fixés par la plateforme](https://research.4pillars.io/en/research/collector-crypt-has-no-collectors). Marge d'environ [8 % du volume marchand après rachats, 5 % après cartes réclamées](https://blockworks.com/api/investor-report/collector-crypto-token-holder-report-q2-2026/pdf) **[Partiel]**.
- **Fermeture sous pression judiciaire.** DraftKings a [arrêté son activité NFT Reignmakers en juillet 2024](https://decrypt.co/242459/draftkings-kills-fantasy-sports-nft-business), en invoquant des « évolutions juridiques récentes », puis [a transigé pour 10 M$](https://decrypt.co/308289/draftkings-agrees-to-settle-nft-lawsuit) **[Vérifié]**.
- **Indices de memecoins : peu d'adoption visible.** [VanEck a lancé un indice MarketVector de six memecoins en mai 2024](https://www.fxstreet.com/cryptocurrencies/news/vaneck-launches-marketvector-memecoin-index-to-track-bonk-floki-doge-pepe-wif-and-shib-tokens-202405090200) (BONK, FLOKI, DOGE, PEPE, WIF, SHIB). Le jeton panier [MEMEX afficherait environ -79 % sur 2026](https://coincodex.com/crypto/meme-index/) **[Partiel]**, page en partie illisible. Aucune fermeture documentée n'a été trouvée, et rien sur un produit Index Coop ou un ETF Bitwise **[Non vérifié]**.
- **Mortalité des jetons.** [53,2 % des jetons de GeckoTerminal sont classés morts, soit 11,6 M sur 20,2 M](https://www.crowdfundinsider.com/2026/01/257221-dead-coins-over-50-of-cryptocurrencies-have-failed-report-reveals/). [Près de 69 % des jetons Pump.fun cessent d'être échangés le jour du lancement](https://crypto.news/pump-funs-token-factory-has-a-69-launch-day-death-rate-coingecko/) **[Vérifié]** (définitions propres à chaque étude).

### 1.4 Ce qui rendrait le projet nouveau

Aucun produit de cartes-memecoins adossées et brûlables n'a été trouvé **[Non vérifié : absence de résultat, pas preuve d'absence]**. Les différences défendables **[Inférence]** :

- **Adossement vérifiable on-chain**, sans coffre, livraison ni valeur assurée fixée par la plateforme : la quantité bloquée se lit dans le contrat.
- **La sortie est financée par le jeton bloqué**, et non par un rachat à un taux décidé par la plateforme.
- **La collection a une place réelle** : les coins morts deviennent un « cimetière » à collectionner, contre-pied de la revente immédiate à 98 %.

**Limite à dire clairement.** La valeur assurée d'une carte Pokémon est relativement stable. Celle d'un memecoin peut tendre vers zéro. La quantité de jetons est garantie, **leur valeur ne l'est pas**. Ne jamais parler de « plancher de valeur ».

---

## 2. Droits sur les images et les noms

### 2.1 Réponse directe à l'équipe : peut-on réutiliser les logos des autres coins ?

**Non par défaut. Tous les visuels doivent être originaux.** Écarter Pepe et Doge ne suffit pas :

- **Aucune licence trouvée.** Les recherches sur BONK, dogwifhat, Shiba, Floki et PENGU n'ont fait ressortir ni licence, ni CC0, ni kit de marque **[Non vérifié : absence de résultat, à contrôler sur chaque site officiel]**. Sans autorisation, l'œuvre reste protégée : le silence d'un projet n'est pas une licence **[Inférence, principe général du droit d'auteur]**.
- **La tolérance entre communautés ne couvre pas une vente.** Le créateur du logo Shiba Inu l'a donné à la communauté, puis [s'est opposé à son usage commercial](https://www.dlnews.com/articles/people-culture/creator-of-shiba-inu-memecoin-dog-logo-fights-commercial-use/).
- **Le seul texte public trouvé n'autorise pas notre usage.** Dogecoin [encourage l'art de fans, y compris vendu, mais refuse l'usage du nom ou du logo à des fins de profit ou laissant croire à un partenariat](https://dogecoin.com/trademarks) **[Vérifié sur extrait tronqué]**.
- **Les créateurs réagissent quand un coin décolle.** Voir Chill Guy et Own The Doge ci-dessous.
- **Détenir le jeton ne donne aucun droit sur l'image**, et une carte vendue au public est un usage commercial direct **[Inférence]**.

**Seule exception : une autorisation écrite** du titulaire réel, couvrant une vente de NFT avec revente. L'accord de la seule communauté du jeton ne suffit pas.

### 2.2 Situation par coin

| Coin | Faits | Statut | Avis |
|---|---|---|---|
| **PEPE** | Matt Furie a fait [retirer d'OpenSea une collection Pepe de 7 000 NFT](https://decrypt.co/78788/pepe-the-frog-meme-nfts-opensea-copyright-dmca?amp=1) (2021) et [obtenu 15 000 $ et l'arrêt des ventes d'Infowars](https://www.npr.org/2019/06/11/731520403/alex-jones-to-pay-15-000-in-pepe-the-frog-copyright-infringement-case). Il [ne semblait pas poursuivre le jeton PEPE en 2023](https://protos.com/pepe-creator-matt-furie-says-he-didnt-know-pepecoin-existed) | **[Vérifié]**, position actuelle **[Non vérifié]** | **Image à éviter.** Précédent NFT direct |
| **BRETT** | Personnage de Furie, [sans lien officiel avec le jeton](https://coinmarketcap.com/cmc-ai/based-brett/what-is) | **[Partiel]** | **Image à éviter** |
| **DOGE, photo de Kabosu** | Photo d'Atsuko Sato. Own The Doge détient [une licence exclusive, pas la propriété](https://goodshibe.substack.com/p/tridog-just-put-the-entire-doge-community). [Plainte déposée le 6 janvier 2026 pour contrefaçon contre Cocoro](https://assets.alm.com/19/8d/58cbebf54723a7c24e22d0735131/doge-v-cocoro-community-project-complaint-u-s-distict-court-for-the-district-of-new-jersey.pdf). Own The Doge [dit ne pas viser les usages existants conformes à l'esprit Dogecoin](https://www.theblock.co/post/289922/dao-buy-dogecoin-shiba-inu-image-nft-dogwifhat) | **[Vérifié]** pour la plainte, issue et portée de la licence **[Non vérifié]** | **Image à éviter.** Droits activement défendus en 2026 |
| **Logo et nom Dogecoin** | [Marques européennes obtenues en janvier 2022](https://cointelegraph.com/news/dogecoin-foundation-registers-name-and-logos-as-trademarked-within-in-the-eu), [demande américaine refusée pour un dessin](https://bitcoinist.com/uspto-rejects-dogecoin-trademark-application) | **[Vérifié]** | **Logo à éviter** en Europe |
| **NEIRO, Cocoro** | [Own The Doge revendique les droits sur l'image de Neiro](https://decrypt.co/296895/doge-meme-pup-owner-ip-move-neiro-coin) | **[Partiel]** | **À éviter** |
| **WIF (dogwifhat)** | Photo prise en 2018 par les propriétaires d'Achi, [NFT vendu 4,3 M$ au trader GCR](https://www.theblock.co/post/283079/dogwifhat-memecoin-iconic-photo-sold-as-nft-for-4-3-million). Qui détient le droit d'auteur après la vente : inconnu | **[Vérifié]** pour la vente, droits **[Non vérifié]** | **Image à éviter.** Titulaire identifiable et intéressé |
| **SHIB** | [Créateur du logo opposé à l'usage commercial](https://www.dlnews.com/articles/people-culture/creator-of-shiba-inu-memecoin-dog-logo-fights-commercial-use/), suites inconnues | **[Partiel]** | **Risqué** |
| **BONK, FLOKI, PENGU** | Rien trouvé sur licence ou marque | **[Non vérifié]** | **Risqué** tant que rien n'est écrit |
| **Chill Guy** | L'artiste [a annoncé des retraits visant les usages lucratifs](https://cointelegraph.com/news/chill-guy-creator-threatens-legal-action-memecoins), puis [accepté l'usage par des marques avec crédit](https://www.theblock.co/amp/post/327554/just-a-chill-guy-legal) | **[Vérifié]** | **À éviter** |
| **Moo Deng** | Le zoo [a déposé des marques, certaines enregistrées](https://sitetest.rouse.com/insights/news/2025/moo-deng-when-thailand-s-beloved-sassy-hippo-played-a-vital-role-in-ip) ; aucune action connue contre le jeton | **[Partiel]** | **À éviter** |
| **Coins à l'effigie de personnes réelles** | Droit à l'image en plus du droit d'auteur, non étudié ici | **[Non vérifié]** | **À éviter** |
| **Memecoins natifs NEAR** (Black Dragon, NEKO, LONK) | Licences non trouvées, mais équipes plus faciles à contacter. Liquidité faible : [paire BLACKDRAGON/wNEAR vers 39 000 $](https://dexscreener.com/near) | **[Partiel]**, chiffre non daté | **Meilleurs candidats à un accord écrit** |

**Aucun coin n'est « sûr » sans autorisation écrite.**

### 2.3 Approche visuelle la plus sûre

1. **Art 100 % original et abstrait.** Par exemple une image générée à partir de l'adresse du contrat et du ticker, avec un cadre de rareté : aucun personnage, chien ni grenouille.
2. **Ne pas imiter.** Une grenouille verte triste ou un chiot en bonnet « redessinés » restent des reprises reconnaissables **[Inférence]**.
3. **Ticker en texte simple**, comme donnée factuelle (« contient X jetons, contrat Y »), sans logo ni police imitée. Le risque de marque n'est pas nul, car le ticker figure sur un produit vendu **[Inférence]**. Les règles d'usage référentiel en droit des marques n'ont pas été vérifiées **[Non vérifié]**.
4. **Mention visible :** « sans lien ni partenariat avec les projets, créateurs ou titulaires cités ».
5. **Prévoir le retrait** : pouvoir changer l'image d'une carte ou retirer un coin des prochains boosters, sans toucher aux jetons bloqués.
6. **Faire vérifier les droits sur l'art lui-même** (auteur, cession écrite, ou outil de génération et ses conditions).

---

## 3. Cadre légal (orientation, pas conseil juridique)

### 3.1 France : prohibition de principe

L'article L320-1 du Code de la sécurité intérieure [répute jeux d'argent les opérations offertes au public qui font naître l'espérance d'un gain dû, même partiellement, au hasard, moyennant un sacrifice financier](https://www.ofdt.fr/sites/ofdt/files/2025-07/note-reglementation-jah_8_1.pdf). Depuis 2019, [le sacrifice est établi dès qu'une avance est exigée, même remboursable](https://www.legifrance.gouv.fr/jorf/id/JORFSCTA000039167505) **[Vérifié]**.

| Critère | Notre produit | Analyse **[Inférence]** |
|---|---|---|
| Offre au public | Site ouvert | Rempli |
| Sacrifice financier | Prix du booster en NEAR | Rempli |
| Hasard | Tirage des cartes | Rempli |
| Espérance de gain | Cartes revendables, jetons récupérables, tirages valant plus que le prix | Très probablement rempli |

- **Position du régulateur sur les loot boxes.** L'ARJEL a conclu en 2018 que [les loot boxes n'étaient pas des jeux d'argent, surtout faute de valeur réelle des objets](https://connectontech.bakermckenzie.com/french-gambling-regulator-releases-its-position-on-loot-boxes). Elle avait aussi évoqué [le cas d'un marché d'échange en argent réel](https://next.ink/8647/105681-loot-boxes-arjel-repond-a-ufc-que-choisir/), sans trancher. **[Vérifié]** Cet argument ne nous protège pas : nos cartes ont une valeur réelle **[Inférence]**.
- **Sorare**, sous [« doutes sérieux » de l'ANJ, a dû faire évoluer son offre](https://www.linfodurable.fr/dans-le-viseur-du-regulateur-des-jeux-sorare-sengage-faire-evoluer-son-offre-35383) **[Vérifié]**, état actuel **[Non vérifié]**.
- **Sanctions.** [Jusqu'à 7 ans et 200 000 € en bande organisée](https://questions.assemblee-nationale.fr/dyn/15/questions/QANR5L15QE14570.pdf) **[Vérifié]**. Peine de base (3 ans et 90 000 €, de mémoire) **[Non vérifié]**.
- **Aucune position de l'ANJ sur les cartes tokenisées ou les boosters numériques** n'a été trouvée **[Non vérifié]**.

### 3.2 France : le régime JONUM

Créé par [l'article 40 de la loi SREN](https://www.legifrance.gouv.fr/jorf/article_jo/JORFARTI000049563458) et rendu applicable par le [décret n° 2026-60 du 4 février 2026](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000053443861). [L'ANJ a lancé l'expérimentation en février 2026](https://anj.fr/lancement-de-lexperimentation-du-cadre-de-regulation-des-jonum). Elle court trois ans à compter de la promulgation de la loi, soit en principe jusqu'au 22 mai 2027 **[Vérifié]**.

| Exigence | Notre produit tel que décrit | Écart |
|---|---|---|
| [Vrai jeu avec progression et interactions](https://www.lofficieldesmetiers.fr/jonum-le-decret-fixant-le-cadre-legal-de-lexperimentation-des-jeux-a-objets-numeriques-est-paru/) | Ouverture de boosters seule | **Bloquant.** Il faudrait une vraie couche de jeu |
| [Objet cessible à des tiers, jamais à l'entreprise ou à une personne agissant de concert](https://anj.fr/jeux-objets-numeriques-monetisables-jonum) ; [article 41](https://www.legifrance.gouv.fr/jorf/article_jo/JORFARTI000049563459) | La revente entre joueurs convient. Le burn contre jetons peut ressembler à un rachat par l'émetteur | **À faire qualifier** **[Inférence]** |
| Pas de gain en monnaie légale | Jetons et non euros : à vérifier | À confirmer |
| [Récompenses accessoires en crypto-actifs MiCA, hors stablecoins : au plus 20 % du chiffre d'affaires du jeu et 25 000 € par joueur et par an](https://www.lofficieldesmetiers.fr/jonum-le-decret-fixant-le-cadre-legal-de-lexperimentation-des-jeux-a-objets-numeriques-est-paru/) | Exemple de la partie 4 : 60 % du prix en jetons | **Bloquant** si le burn est une « récompense accessoire » **[Inférence]** |
| Mineurs interdits, prévention du jeu excessif, de la fraude et du blanchiment | À construire | À prévoir |
| [Déclaration préalable à l'ANJ](https://anj.fr/sites/default/files/2026-02/D%C3%A9cision%20n%C2%B02026-026_JONUM_DossierD%C3%A9clarationPr%C3%A9alable.pdf), [siège dans l'UE, en Islande, au Liechtenstein ou en Norvège](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000053443861), [message de mise en garde](https://www.anj.fr/sites/default/files/2026-06/D%C3%A9cision%20n%C2%B02026-133_JONUM_MessageMiseEnGarde.pdf) | À faire | À prévoir |

**Conclusion [Inférence].** Le produit tel que décrit n'entre pas dans JONUM. Une version compatible serait un vrai jeu, avec des jetons limités à environ 20 % du chiffre d'affaires, et un burn dont la nature serait validée. C'est un autre produit, avec une expérimentation qui finit dans environ six mois sauf prolongation. Le décret complet reste à lire.

### 3.3 Union européenne

- **MiCA et NFT.** [MiCA exclut les crypto-actifs uniques et non fongibles](https://www.springlex.eu/en/packages/mica/mica-regulation/article-2/), avec [une analyse au cas par cas](https://www.fma.gv.at/en/?p=442746) **[Vérifié]**. Des commentateurs indiquent que [l'émission en grande série est un indice de fongibilité](https://www.taylorwessing.com/en/insights-and-events/insights/2022/10/regulation-of-nfts-in-the-eu) (considérant à relire au Journal officiel) **[Partiel]**. ESMA [regarde la fonction économique et non l'étiquette](https://www.bdo.com.mt/en-gb/news/news-in-2025/understanding-the-esma-guidelines-on-crypto-assets-as-financial-instruments) **[Vérifié]**.
- **Application à notre carte [Inférence].** Des cartes de même coin et même rareté, dont la valeur vient d'une quantité de jetons fongibles, risquent de ne pas être « uniques ». Le numéro de série n'y change rien. Il faudrait au minimum des quantités et attributs réellement distincts, et même cela ne garantit rien.
- **Services sur crypto-actifs.** Acheter des jetons pour l'utilisateur et les conserver peut ressembler à de l'échange ou de la conservation **[Inférence]**. Depuis le 1er juillet 2026, [un prestataire sans agrément MiCA doit cesser en France, sous peine de 2 ans et 30 000 €](https://www.amf-france.org/fr/actualites-publications/actualites/lamf-rappelle-que-la-periode-transitoire-pour-les-psan-pour-continuer-de-fournir-des-services-sur) **[Vérifié]**. Aucune analyse n'a été trouvée sur un NFT remboursable en jetons fongibles, ni sur un contrat non géré par une entité **[Non vérifié]**.
- **Loot boxes : pas de règle commune.** Belgique : [illégales selon le régulateur en 2018](https://www.pcgamer.com/belgiums-gambling-commission-rules-against-loot-boxes-in-overwatch-fifa-18-and-csgo/). Pays-Bas : [non jeu de hasard pour FIFA en 2022, le jeu étant surtout d'adresse](https://cms.law/en/nld/legal-updates/dutch-court-rules-fifa-loot-boxes-not-a-game-of-chance-revokes-ea-penalty). Autriche : [même logique, Cour suprême, 18 décembre 2025](https://www.dlapiper.com/insights/publications/2026/01/supreme-court-shifts-the-playing-field-lootboxes-fall-outside-the-austrian-gambling-act) **[Vérifié]**. Ces décisions s'appuient sur l'adresse dans un jeu plus large. Un booster pur n'a pas cet argument **[Inférence]**.
- **Tendance au durcissement.** [Action du réseau CPC visant neuf sociétés de jeu vidéo](https://www.lewissilkin.com/insights/2026/10/15/eu-consumer-protection-network-launches-action-involving-nine-video-games-compani-102o5do) **[Partiel]**. Le Digital Fairness Act [pourrait aller jusqu'à interdire les récompenses aléatoires](https://technologyquotient.freshfields.com/post/102ltio/the-eus-proposed-digital-fairness-act-a-game-developers-guide-to-potential-imp) ; publication attendue fin 2026, non confirmée **[Non vérifié]**.

### 3.4 États-Unis

**Valeurs mobilières**
- Le personnel de la SEC a indiqué le 27 février 2025 que [les memecoins ne sont généralement pas des valeurs mobilières](https://sec.gov/newsroom/speeches-statements/staff-statement-meme-coins). Le 17 mars 2026, [une interprétation commune SEC-CFTC classe NFT et memecoins en « objets de collection numériques »](https://www.orrick.com/en/insights/2026/04/sec-issues-interpretive-guidance-on-crypto-asset-classification), avec [réserve pour le fractionnement lié aux efforts d'un tiers et les contrats d'investissement](https://www.jenner.com/en/news-insights/client-alerts/sec-and-cftc-issue-landmark-joint-interpretation-on-crypto-asset-classification) **[Vérifié]**.
- Précédents plus anciens : [Dapper, 4 M$](https://decrypt.co/233621/dapper-labs-reaches-4-million-settlement-nba-top-shot-nft-lawsuit), [DraftKings, 10 M$](https://decrypt.co/308289/draftkings-agrees-to-settle-nft-lawsuit), [Impact Theory, environ 6,1 M$](https://www.omm.com/insights/alerts-publications/sec-s-impact-on-nfts-is-more-than-theory-first-enforcement-action-against-an-nft-creator/), [Stoner Cats](https://frblaw.com/nft-firsts-sec-settles-first-two-nft-securities-cases/) **[Vérifié]**. Leçon : ne jamais vendre un rendement ou une hausse **[Inférence]**.
- [Le CLARITY Act n'est pas adopté et cale au Sénat](https://www.orrick.com/fr-FR/Insights/2026/10/The-CLARITY-Act-Stalls-in-the-Senate-Whats-Next-for-Digital-Asset-Regulation) **[Vérifié sur titre et sources d'octobre 2026]**.

**Jeux d'argent : le risque principal**
- Test classique : [contrepartie, hasard, lot de valeur](https://womblebonddickinson.com/us/insights/alerts/chase-trading-card-repacks-face-growing-legal-scrutiny). Le produit remplit les trois **[Inférence]**.
- [Demandes d'arbitrage contre Whatnot en mars 2026](https://www.casinoreports.com/news/whatnot-gambling-charges-california/) (Code pénal californien § 319, RICO), sans décision à ce jour. La Californie vise aussi [les « grab bags » de cartes de sport](https://www.womblebonddickinson.com/us/insights/insights/102o3q3/the-future-of-card-breaking-and-repacks-insights-from-california-litigation) **[Vérifié]**.
- [New York poursuit Valve depuis février 2026](https://www.techspot.com/news/111659-valve-loot-boxes-more-like-trading-cards-than.html). Valve compare ses caisses aux boosters de cartes, et l'État répond que ces objets ont une valeur **[Vérifié]**.
- Une source mentionne [des poursuites visant aussi Collector Crypt](https://on360.ca/?p=920), en partie rédigée par IA **[Non vérifié]**.

### 3.5 Comment font les produits comparables

Ce qui est documenté : affichage de l'espérance, mention que [le rachat n'est pas un profit](https://docs.jup.ag/user-docs/trade/gacha/instant-buyback), et rachat à taux public. Le dirigeant de Collector Crypt reconnaît que ses machines [peuvent être vues comme repoussant les limites du droit des jeux](https://cointelegraph.com/features/pokemon-cards-as-rwas-gacha-spending-hits-records-as-crypto-sinks) **[Partiel]**. La taille de ces acteurs montre une tolérance de fait, **pas une légalité**.

**[Non vérifié]** : blocages géographiques, États exclus, mécanisme d'entrée gratuite, conditions d'utilisation de Courtyard et Collector Crypt. La publication des probabilités par Courtyard est [contradictoire selon les sources](https://thecardshopfinder.com/guides/pack-ripping/courtyard-io-review/).

---

## 4. Économie

### 4.1 Références de raretés

| Référence | Donnée | Statut |
|---|---|---|
| Pokémon physique | [Pas de taux publiés](https://www.magicmadhouse.co.uk/pokemon-tcg-scarlet-and-violet-pull-rates). Communauté : double rare environ 1 sur 7, illustration rare environ 1 sur 13, spéciale environ 1 sur 32 à 1 sur 47 | **[Partiel]** |
| Magic Play Booster | [Poids par défaut : 60 rares pour 20 mythiques](https://mtg.wiki/page/Play_Booster), soit 3 pour 1, variable selon l'extension | **[Partiel]** |
| Pokémon TCG Pocket (5 cartes) | [Booster rare 0,05 %](https://pokemongohub.net/post/guide/pokemon-tcg-pocket-pull-rates-explained/). Le 5e emplacement est [environ 4 fois plus favorable que le 4e](https://finalboss.io/pokemon-trading-card-game-pocket-ruler-of-the-skies-b4-pull-odds-guide) | **[Partiel]**, le tableau officiel est dans l'application |
| Genshin Impact | [0,6 % de base, 1,6 % en moyenne avec garantie, garantie au 90e tirage](https://genshin-impact.fandom.com/wiki/Wish) | **[Partiel]** wiki de fans |
| Publication des taux | [Exigée par Apple depuis fin 2017](https://www.animenewsnetwork.com/interest/2018-01-20/apple-requires-apps-to-disclose-odds-for-gacha-loot-box-purchases/.126613), [obligation légale en Corée depuis mars 2024](https://shattered.io/loot-box-odds-disclosure-laws-2026/). [Le « kompu gacha » est interdit au Japon depuis 2012](https://wikipedia.com/wiki/Gacha_game) | **[Partiel]** |
| Retour au joueur | Collector Crypt : [environ 90,6 % rendus](https://research.4pillars.io/en/research/collector-crypt-has-a-margin-problem). Rachats 85 à 93 % | **[Partiel]** |

### 4.2 Conséquences de l'achat à l'ouverture

| Conséquence | Détail **[Inférence]** |
|---|---|
| Positif : pas de stock | Aucun jeton à acheter d'avance, donc aucun risque de baisse pour la trésorerie |
| Positif : pas d'oracle | Prix du booster et valeur des cartes sont en NEAR. La quantité de jetons est ce que l'échange a réellement livré |
| Positif : pas d'arbitrage de date | Avec une quantité fixe, l'acheteur attendrait une hausse du jeton pour ouvrir. Avec une valeur fixée en NEAR, l'instant d'ouverture n'apporte rien |
| Négatif : réserve nécessaire | Un gros tirage coûte plus que le prix du booster |
| Négatif : achats prévisibles | Un bot peut acheter avant l'achat du contrat, puis revendre |
| Négatif : profondeur des pools | Un gros achat fait monter le prix payé |
| Négatif : tirage et échange ne sont pas atomiques | Il faut un cas clair d'échec de l'achat |

### 4.3 Formules

Notation : `P` prix du booster, `n` cartes, `d` part de cartes de coins morts, `q` part des cartes vivantes brûlables, `p_r` probabilité de la rareté, `w_r` poids de la rareté, `m` multiplicateur de quantité (moyenne `E[m]`), `β` part d'adossement visée.

**Valeur en NEAR à acheter pour une carte brûlable :**

```
v = κ · w_r · m
κ = β·P / ( n · (1−d) · q · Σ(p_r·w_r) · E[m] )
```

**Valeur nette maximale d'un attaquant qui brûle tout :**

```
c = (1 − s_achat) · (1 − f_burn) · (1 − s_vente)
A = β·P·c + n·(1 − (1−d)·q)·μ·(1 − φ)
```

avec `s_achat` et `s_vente` les coûts d'échange, `f_burn` les frais de burn, `μ` le prix moyen de revente d'une carte non brûlable, `φ` les frais de marché.

**Condition anti-arbitrage**, avec une marge de sécurité `ε` :

```
A ≤ P·(1 − ε)   ⇔   β ≤ ( P·(1−ε) − n·(1−(1−d)·q)·μ·(1−φ) ) / ( P·c )
```

**Limite de profondeur.** Sur un pool à produit constant avec `x` NEAR de réserve, le surcoût moyen d'un achat `v` vaut environ `v/x`, hors frais :

```
v ≤ s_max · x
```

**Réserve de départ** (approximation normale, fragile car la distribution a une queue épaisse) :

```
R₀ ≈ V_cap + (z·σ)² / (4·δ)
```

avec `V_cap` le paiement maximal d'un booster, `σ` l'écart-type de l'adossement d'un booster, `δ` la part par booster affectée à la réserve, `z` le niveau de prudence.

### 4.4 Exemple travaillé (tous les paramètres sont illustratifs)

**[Illustratif]** `P = 10 NEAR`, `n = 5`, `d = 20 %`, `q = 60 %`, `β = 60 %`, multiplicateur `m` de 0,5 (40 %), 1 (40 %) ou 2 (20 %), donc `E[m] = 1`.

Une carte est brûlable avec une probabilité de `0,8 × 0,6 = 48 %`, quelle que soit sa rareté.

| Rareté | Probabilité par carte | Poids et valeur `v` de base (NEAR, κ = 1) | Contribution `p·w` |
|---|---:|---:|---:|
| Commune | 70 % | 1 | 0,70 |
| Peu commune | 20 % | 2 | 0,40 |
| Rare | 8 % | 8 | 0,64 |
| Épique | 1,8 % | 30 | 0,54 |
| Légendaire | 0,2 % | 110 | 0,22 |
| **Total** | **100 %** | | **2,50** |

**Vérification.** `κ = (0,6 × 10) / (5 × 0,48 × 2,50 × 1) = 6 / 6 = 1`. L'adossement moyen est de 1,2 NEAR par carte, soit **6,0 NEAR par booster**.

**Répartition moyenne des 10 NEAR**

| Poste | NEAR | Part |
|---|---:|---:|
| Achat de jetons bloqués | 6,00 | 60 % |
| Réserve de variance | 1,00 | 10 % |
| Exploitation (gaz, aléa, infrastructure) | 0,50 | 5 % |
| Licences ou créateurs éventuels | 0,50 | 5 % |
| Marge de l'équipe | 2,00 | 20 % |
| **Total** | **10,00** | **100 %** |

**Probabilités qui en découlent**

| Événement | Calcul | Résultat |
|---|---|---:|
| Au moins une carte Rare ou mieux | `1 − 0,9⁵` | 41 % |
| Au moins une Légendaire, brûlable ou non | `1 − 0,998⁵` | 1,0 % |
| Au moins une Légendaire brûlable | `1 − (1 − 0,00096)⁵` | 0,48 %, environ 1 sur 209 |
| Aucune carte brûlable | `0,52⁵` | 3,8 % |
| Adossement du booster ≥ 10 NEAR | estimation manuelle | environ 14 %, à simuler |

**Variance.** `E[V²] = 47,02` et `E[m²] = 1,3`, donc la variance d'une carte vaut `0,48 × 47,02 × 1,3 − 1,2² = 27,90`. Pour le booster : `σ ≈ √(5 × 27,90) ≈ 11,8 NEAR`, pour une moyenne de 6. Le booster typique contient autour de 3 NEAR de jetons (ordre de grandeur à simuler). Les tirages rares portent la moyenne.

**Test « j'achète puis je brûle tout »**, avec `s_achat = 1,5 %`, `f_burn = 2 %`, `s_vente = 3 %`, `μ = 0,3 NEAR`, `φ = 5 %` **[Illustratif]** :

```
c = 0,985 × 0,98 × 0,97 = 0,9363
Burn net  = 6,00 × 0,9363 = 5,62 NEAR
Reventes  = 5 × 0,52 × 0,3 × 0,95 = 0,74 NEAR
A = 6,36 NEAR pour 10 payés, soit −3,64 NEAR en moyenne
```

Avec `ε = 15 %`, la borne est : `β ≤ (8,5 − 0,741) / (10 × 0,9363) = 82,9 %`.

**Sensibilité à β**

| β | Adossement moyen | Burn net | Reste pour réserve, exploitation et marge |
|---:|---:|---:|---:|
| 60 % | 6,00 | 5,62 | 4,00 |
| 75 % | 7,50 | 7,02 | 2,50 |
| 85 % | 8,50 | 7,96 | 1,50 |

Une valeur de 60 % reste très inférieure aux 85 à 93 % de rachat du marché. Le joueur compare, mais ces rachats portent sur une valeur assurée. Un β élevé rapproche aussi le produit d'une promesse de gain **[Inférence]**. Le cap légal de 20 % du régime JONUM est incompatible avec ces trois niveaux.

**Réserve [Illustratif].** Le maximum théorique d'un booster est de 1 100 NEAR (5 Légendaires × 220). Un plafond de `V_cap = 250 NEAR` a un effet négligeable sur l'espérance et favorise la maison. Avec `z = 3`, `σ = 11,8`, `δ = 1` : `R₀ ≈ 250 + (3 × 11,8)² / 4 ≈ 564 NEAR`. **Si la réserve descend sous `V_cap`, on suspend les ventes.** On ne modifie jamais les probabilités en silence.

**Profondeur [Illustratif].** Une Légendaire de 110 à 220 NEAR avec `s_max = 2 %` exige un pool de 5 500 à 11 000 NEAR de réserve. Les hautes raretés doivent donc être limitées aux pools profonds. Le support de memecoins par NEAR Intents n'est pas confirmé **[Non vérifié]** ; [le volume global du service est élevé](https://defillama.com/protocol/near-intents?denomination=NEAR).

### 4.5 Parades contre les arbitrages

| Attaque | Parade |
|---|---|
| Espérance de burn supérieure au prix | Respecter la borne sur `β`, publier les paramètres |
| Voir le tirage puis annuler | Paiement engagé d'abord, aléa issu d'un bloc ultérieur, aucune annulation ensuite |
| **Faire échouer l'achat après un mauvais tirage pour être remboursé** | **Jamais de remboursement une fois le tirage connu** : en cas d'échec, nouvelle tentative, ou la carte reste adossée en NEAR |
| Manipulation de l'aléa par un validateur | [La documentation NEAR prévient que le producteur de bloc peut l'exploiter](https://docs.near.org/smart-contracts/security/random). Acceptable en démonstration, à durcir pour de vraies valeurs **[Vérifié]** |
| Front-running de l'achat | Limite `s_max`, petits montants par coin, plafond de valeur par pool |
| Pompage du pool avant ouverture | Exclure les coins sous un seuil de liquidité, ne pas acheter si le prix s'écarte trop d'une moyenne récente |
| Burn immédiat puis vente | Délai de burn (24 à 72 h **[Illustratif]**) ; cela limite la revente instantanée, sans remplacer la borne sur `β` |
| Carte brûlable vendue sous sa valeur | Pas une perte pour le protocole : les jetons sont déjà bloqués |
| Coin qui meurt après le blocage | Le burn rend des jetons sans valeur. À afficher avant l'achat |

---

## 5. Recommandations

1. **Hackathon : testnet ou démonstration fermée, sans vente au public de valeurs réelles.** C'est la seule façon simple d'écarter le sacrifice financier et l'offre au public **[Inférence]**.
2. **Tous les visuels sont originaux**, générés de façon abstraite, avec ticker en texte, mention de non-affiliation et possibilité de retrait. Aucun logo sans accord écrit.
3. **Tester une demande d'accord écrit** auprès d'une ou deux équipes de memecoins natifs NEAR, ce qui donne un exemple propre pour la démonstration.
4. **Garder la décision d'achat à l'ouverture, avec une valeur fixée en NEAR**, et écrire les règles : paiement puis aléa, aucun remboursement après tirage, limite par pool, plafond par booster, arrêt des ventes si la réserve est insuffisante.
5. **Prendre `β` entre 60 et 70 % au départ**, garder `ε ≥ 15 %`, et simuler avant de fixer les raretés.
6. **Publier les probabilités, l'adossement moyen et le fait que la plupart des boosters valent moins que leur prix.** Dire « quantité de jetons », jamais « valeur garantie », « rendement » ou « investissement ».
7. **Restreindre les hautes raretés aux coins liquides** et définir une règle objective pour « coin mort » (liquidité et volume sur une durée).
8. **Avant toute mise en production :** avis d'avocat sur L320-1, JONUM et MiCA, lecture complète du décret, restriction d'âge et de pays.

## 6. Risques ouverts

| Risque | Niveau | État |
|---|---|---|
| Qualification de jeu d'argent interdit en France | Très élevé | Non résolu, aucune position de l'ANJ trouvée sur ce type de produit |
| Incompatibilité avec JONUM (jeu, plafond de 20 %, rachat par l'émetteur) | Très élevé | À faire confirmer sur le décret complet |
| Loterie illégale aux États-Unis | Élevé | Litiges en cours, sans décision |
| Statut MiCA des cartes et service sur crypto-actifs | Élevé | Aucune analyse trouvée sur ce montage |
| Durcissement européen (Digital Fairness Act) | Moyen à élevé | Texte attendu, non confirmé |
| Fin de l'expérimentation JONUM vers mai 2027 | Moyen | Prolongation inconnue |
| Droits d'auteur et marques, y compris sur les tickers | Élevé avec logos, moyen sans | Aucune licence trouvée |
| Liquidité très faible des memecoins NEAR, chiffres non datés | Élevé | À mesurer directement |
| Valeur des jetons bloqués qui tend vers zéro | Élevé | Inhérent au produit, à afficher |
| Réserve insuffisante (queue épaisse) | Moyen | Simulation à faire, formule approximative |
| Aléa NEAR manipulable par un validateur | Faible en démonstration, moyen en production | Solution à concevoir |
| Demande limitée à la revente immédiate | Moyen | Constaté chez les comparables |
