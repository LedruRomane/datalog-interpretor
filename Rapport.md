# Projet Developing a Datalog Engine Extension for aggregate functions.

Projet développé par LEDRU Romane P2105081

## Installation

> ATTENTION **Python3** sera nécessaire au lancement et au test de ce projet. 

1. Dans le répertoire /Prog vous y trouverez les fichiers .py du programme ainsi que le main, ouvrez un terminal à cet emplacement afin de lancez celui-ci.
2. Le programme demande un fichier datalog en entrée. Les fichiers de tests se trouvent dans ./tests
3. Pour tester le programme il vous faudra lancer cette commande : 

```bash 
python3 main.py -f tests/NomduFichier.dl
```

L'extention .dl des fichiers correspond à un fichier datalog.

---


## Partie 1 : Preprocessing 

### 1-  Choix profil datalog : 
> 
> 1 - Fichiers tests doivent être au format .dl
>
> 2 - Deux parties distinctes du fichier doivent être présente : 
>
>       Les EDB listés.
> 
>       Les IDB listés (Q1, Q2, etc) et stratifiés (ordonnancement correct), avec :- dans leur définition.
>
> 3 - Les prédicats commencent tous par une majuscule et sont séparés d'une virgule seulement. Les variables sont elles en majuscules pour ne pas confondre avec une véritable valeur statique.

Structure imposée: 

- Pas de not.

Pour les fonction d'aggregation on ajoutera dans les IDB des prédicats avec (x, y) dont le x est l'indice utilisé dans la fonction et le y le nom de la fonction contenant les valeurs retournées.

Fonction d'aggregations disponibles :  
- Count(x, Count)
- Min(x, Min)
- Max(x, Max)
- Sum(x, Sum)
- Avg(x, Avg)


Fonctions de comparaisons disponibles : 
- E1 < E2
- E1 =< E2
- E1 > E2
- E1 >= E2
- E1 =:= E2 (valeur de E1 =  valeur de E2, une autre façon de faire une comparaison d'égalité stricte mais en l'explicitant) 
- E1 =\= E2 (valeur de E1 != valeur de E2)

On laissera le soin à l'utilisateur de créer un datalog **correct** avec les contraintes ci-dessus.

Différents fichiers dans le dossier test ont été préparés afin de tester le programme dans différentes configuration, libre au correcteur de les utiliser pour visualiser rapidement l'execution.


### 2- Parsing : 

**parse_input_file.py** permet de prendre en entrée le fichier et itérer sur chacune de ses lignes afin d'en extraire les EDB d'un côté, et les IDB split avec la Head et le Body de l'autre.

J'ai choisi de parser en objet EDB, IDB contenant des Predicats.
Les paramètres sont eux parsés en string ou number.
On pourra voir les structures dans les différents fichiers Idb.py, Edb.py, Predicate.py et l'import et le parser (-> number & string) dans Tools.py.

> Note : Par soucis de visualisation, au lancement du programme, on verra dans la console le print du contenu parsé des EBD, IDB et Predicats.

---


## Partie 2 : Evaluation

Création du moteur d'evaluation pour notre datalog.

Pour ce faire on va créer un fichier **evaluation_progam.py** qui prendra en entrée les données retournées de notre parser, et qui évaluera les IDB et retournera les réponses.
### Le dataframe : 
>**Point technique n°1** : Pour gérer les données, on parsera de nouveau les données dans un Dataframe.


-Avantages- : On aura pas à gérer de façon "sale" les jointures, et on gardera une certaine optimisation niveau mémoire.

-Inconvénients- : On rajoute une librairie sur le projet, ce qui implique une installation supplémentaire pour l'utilisateur.

### La récursivité :
>**Point technique n°2 :** : On sait que dans un datalog on a parfois des IDB recursifs tel que : ancestor(X,Y) :- parent.., ancestor(..). Pour gérer le cas de la récursivité, on évalue d'abord une première fois les IDB, et on les ajoutes à notre dataframe. Tant que la sortie n'appartient pas au dataframe (aka n'existe pas encore déjà), on l'ajoute. Dès que la sortie existe déjà, on arrête la récursivité et on retourne le dataframe. 

### L'évaluation :
>**Point technique n°3** : On procède en 4 étapes :
- 1 - Récupération de tous les prédicats atomiques concernés par le body de l'IDB.
- 2 - On filtre d'abord en amont les valeurs statiques renseignées dans le body et on ne garde que les lignes concernées.
- 3 - On merge toutes les colonnes avec cross, c'est un merge force qui rends toutes nos combinaisons possibles sans même s'occuper de la jointure.
- 4 - Puis on s'occupe de la jointure, ça consiste à faire matcher les valeurs des colonnes, appelé token, Z avec Z par exemple (merge_dataframes). Un token est un nom de colonne unique que l'on souhaite filtrer, puis on retire les redondance (filterTable) en loopant sur les tokens pour que les tokens identiques matchent en ayant la même valeur.

### Les fonctions compare : 
>**Point technique n°4** : Pour les fonctions de comparaisons, on ira créer un Prédicat particulier, que l'on nommera ComparisonPredicate, qui héritera de ce qu'est un predicat de base. 
Il prendra 3 paramètres, une valeur, un opérateur de comparaison, et une valeur, dans cet ordre.
L'opérateur de comparaison fonctionnera tel qu'ils sont décrit dans la documentation datalog, ils fonctionneront sur les entier, et seul le =:= et le =\= fonctionnera sur les string. 

Au sein du fichier Predicate.py, on spécifie directement de quel opérateur de comparaison il s'agit afin de le traiter directement à l'étape 4 de l'évaluation.

### Les fonctions d'aggregation :
>**Point technique n°5** : Pour les fonctions d'aggregation, on ira créer un Prédicat particulier, que l'on nommera AggregationPredicate, qui héritera de ce qu'est un predicat de base.

*Problématique* : Comment, dans le cas où on a une fonction de comparaison sur une aggregation, on ordonnance l'évaluation ? 
*Solution* : on a décidé d'ordonnancer dans l'ordre qui suit :
- 1 : les atomes de base,
- 2 : les comparaisons (colonne/colonne, colonne/valeur, valeur/colonne, valeur/valeur),
- 3 : les aggregations, 
- 4 : si la comparaison travaille sur une aggregation, on le fait à la toute fin.

IDB(A, SUM) :- EDB_1(A , _ , _),  --> 1
                EDB_2(B, _ , B2),  --> 1
                A =:= B ,         --> 2
                Sum(B2, SUM),    --> 3
                SUM > 10.       --> 4