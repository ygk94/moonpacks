# Consigne commune : recherche catalogue v2 (11/11/2026)

## Le projet en deux lignes
Memaster : boosters payés en NEAR de 5 cartes NFT, chaque carte = un memecoin de n'importe quelle chaîne.
Lire `README.md` et `docs/catalogue-final.md` (catalogue actuel, 786 cartes + 77 « À décider ») pour le contexte.

## Ce que veut le porteur du projet (non négociable)
- **100 % mèmes.** Pas de jeton utilitaire, DeFi, L1, launchpad, agent IA « sérieux », tap-to-earn, stablecoin.
  Un jeton d'agent IA ou de jeu Telegram n'entre que si c'était d'abord un mème assumé (à justifier).
- **Surtout des anciens** qui ont explosé, ont rendu des gens riches, et ne valent plus rien aujourd'hui. Toutes les
  époques (2013 → 2026), **toutes les chaînes**.
- **Rareté v2 :**
  | Rareté | Règle |
  |---|---|
  | mythique | réservé à DOGE, SHIB, PEPE. Ne pas en proposer d'autre |
  | légendaire | prime de fou : pic ≥ 1 Md$ de capitalisation, **ou** histoire légendaire (×1 000 et plus, millionnaires connus, épisode culte), quel que soit l'état actuel |
  | épique | pic de 100 M$ à 1 Md$, ou histoire marquante |
  | rare | pic de 10 à 100 M$ |
  | commune | mèmes **complètement claqués** (morts, -95 % ou plus, plus de volume) au pic modeste ; c'est la grosse masse |
- La disponibilité sur NEAR Intents **ne compte pas** pour le choix. La liquidité actuelle non plus.

## Drapeaux (ne pas exclure, signaler)
Colonne `Drapeau` : `arnaque avérée` (condamnation ou rug documenté), `politique` (personnalité ou campagne),
`personne réelle` (célébrité), `obscène` (nom obscène ou raciste), vide sinon. Le porteur décidera.

## Format de sortie (obligatoire)
Un fichier markdown, chemin indiqué dans ta mission, avec :
1. 3 à 5 lignes de méthode et de limites.
2. Un tableau, une ligne par jeton :

| Nom | Ticker | Chaîne | Lancement | Pic de capitalisation (date) | Nature du pic | État actuel | Chute depuis le pic | Histoire (1 phrase : l'ascension, qui s'est enrichi, la mort) | Rareté proposée | Drapeau | Source |

- `Nature du pic` : `sourcé` (source citée), `estimé` (calcul, méthode dite), `inconnu`.
- `État actuel` : `mort`, `en déclin`, `actif`, `à vérifier`.
- `Source` : au moins une URL par ligne quand c'est possible ; sinon « connaissance générale, à vérifier ».
- Pas d'invention : un chiffre non trouvé s'écrit « inconnu ». Préférer moins de lignes fiables que des lignes inventées.
- Ne pas répéter un jeton déjà au catalogue actuel **sauf** pour corriger sa rareté ou son histoire : mets-le alors dans un
  second tableau « Corrections de cartes existantes » (N° de carte, champ, ancienne valeur, nouvelle valeur, source).

## Règles de travail
- Écris **uniquement** dans ton fichier de sortie. Ne modifie aucun autre fichier, ne fais pas de `git commit`.
- N'utilise ni clé ni compte. API publiques autorisées (CoinGecko, DexScreener, etc.) avec un User-Agent générique,
  en respectant les limites de débit.
- Écris en français, phrases courtes.
- Ta réponse finale (le récap) : 10 lignes maximum, avec le nombre de lignes par rareté, les 10 trouvailles les plus
  fortes et les doutes principaux.
