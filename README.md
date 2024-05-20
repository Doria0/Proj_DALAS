# Proj_DALAS

https://drive.google.com/file/d/13MSj5_jE6T19rL0QlaIGahEQZx3tVhY4/view?usp=share_link

### Sources de Données
- [IMDb Non-Commercial Datasets](https://developer.imdb.com/non-commercial-datasets/)
- Wikipédia(fr) de certains films (Distribution : Voix originales VS Voix françaises ?)
- Wikipédia(en) (pays, mois de sortie, durée du film, budget, box-office)

Réflexion/recommendation de films à succès en fonction : 
* Genres du film
* Région/Pays de production
* Acteurs
* Producteurs/Directeurs,...
* Voix originales/Voix françaises
* Mois de sortie
* Durée du film (discrétisation par tranches de 30min ?)
* Budget
* (Saga / Plusieurs films de la même série)

Critères de score : 
- Moyenne d’avis
- Nombre de visionnage/Nombre de votes
- Box-office

Axes : 
+ Déterminer les meilleures caractéristiques
+ Estimer les revenus/box-office (en estimant le budget en fonction de l’équipe/des caractéristiques)


## Scrapper
Étant donné que le marché du cinéma évolue très rapidement, pour atteindre nos objectifs, nous prévoyons d'analyser des données actuelles. Initialement, nous avons choisi d'extraire et d'analyser les données des films des cinq dernières années. Nous avons extrait de l'ensemble de données IMDB les films de 2020 à 2024 et constaté que, sur 250 000 films, seulement 1 428 disposaient à la fois de données sur les recettes au box-office et d'une page Wikipédia. Après avoir tracé la distribution des données de ces films, nous avons trouvé que la forme n'était pas claire, nous avons donc décidé d'ajouter davantage de données.

## EDA
Tout d'abord, réalisez une jointure naturelle entre le jeu de données extrait et le jeu de données `title.basics.tsv`. Les principales caractéristiques incluent :

- Box-office, budget, genre, langue, date de sortie (année/mois/jour), durée
- Les réalisateurs, acteurs et autres membres de la production de différents pays

### Distribution des données, corrélation des variables

#### Quantitatives :

- Box-office : histogramme et estimation de densité par noyau
- Budget : ..
- Durée : ..

Il est possible de calculer directement la matrice de covariance entre les variables quantitatives => tracer une carte de chaleur pour voir directement les corrélations.

#### Qualitatives :

Il est nécessaire de coder d'abord les différentes modalités des variables, par exemple en utilisant des vecteurs one-hot, puis d'utiliser la PCA pour réduire la dimensionnalité de la matrice creuse correspondant à toutes les valeurs de cette variable.

- Catégories de films :

  - Y a-t-il un genre dont le revenu moyen du box-office est particulièrement élevé, ce qui pourrait indiquer une popularité plus grande ?

- Date de sortie (année/mois/jour) :

  Idée :

    - La saison (par exemple, l'été, Noël) a-t-elle un impact sur les recettes du box-office ? Y a-t-il des mois où les recettes sont systématiquement plus élevées que les autres ? Ce phénomène pourrait-il être causé par des facteurs autres que la saison, comme la sortie d'une grande production ? **Faut-il contrôler les variables ?**

  > Si un contrôle des variables est nécessaire, on peut stratifier les autres variables non pertinentes, puis réaliser des statistiques sur les variables pertinentes pour réduire leur impact sur les résultats.

- Les petits films sortis dans le même intervalle de temps (par exemple, dans le même mois ou dans une fenêtre de deux semaines) sont-ils affectés par les blockbusters ? (Si oui, lors de la planification de notre sortie, nous devrions négocier avec d'autres studios pour éviter de sortir en même temps et impacter mutuellement le box-office)

- Impact du pays sur le box-office : quelles sont les attentes pour les réalisateurs français, américains, etc. ? :slightly_smiling_face: (Comparaison latérale

  Possible : Quels réalisateurs et acteurs français ont un box-office élevé ?


## Prédiction du box-office 

ex.XGBoost, pour apprendre les corrélations entre les variables et extraire les vars le plus importantes...



