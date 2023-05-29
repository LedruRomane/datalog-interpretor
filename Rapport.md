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
> 3 - Les prédicats commencent tous par une majuscule et sont séparés d'une virgule seulement.

Structure imposée: 

- Pas de not.

Pour les fonction d'aggregation on ajoutera dans les IDB des prédicats avec (x, y) dont le x est l'indice utilisé dans la fonction et le y le nom de la fonction contenant les valeurs retournées.

Fonction d'aggregations disponibles :  
- count(x, Count)
- min(x, Min)
- max(x, Max)
- sum(x, Sum)
- avg(x, Avg)

On laissera le soin à l'utilisateur de créer un datalog **correct** avec les contraintes ci-dessus.

Différents fichiers dans le dossier test ont été préparés afin de tester le programme dans différentes configuration, libre au correcteur de les utiliser pour visualiser rapidement l'execution.


### 2- Parsing : 

**parse_input_file.py** permet de prendre en entrée le fichier et itérer sur chacune de ses lignes afin d'en extraire les EDB d'un côté, et les IDB split avec la Head et le Body de l'autre.

J'ai choisi de parser en objet EDB, IDB contenant des Predicats.
Les paramètres sont eux parsés en string ou number.
On pourra voir les structures dans les différents fichiers Idb.py, Edb.py, Predicate.py et l'import et le parser (-> number & string) dans Tools.py.

> Note : Au lancement du programme, on verra dans la console le print du contenu parsé des EBD, IDB et Predicats.

---


## Partie 2 : Evaluation

Création du moteur d'evaluation pour notre datalog.

Pour ce faire on va créer un fichier **evaluation_progam.py** qui prendra en entrée les données retournées de notre parser, et qui évaluera les IDB et retournera les réponses.

**Point technique n°1** : Pour gérer les données, on parsera de nouveau les données dans un Dataframe.


-Avantages- : On aura pas à gérer de façon "sale" les jointures, et on gardera une certaine optimisation niveau mémoire.

-Inconvénients- : On rajoute une librairie sur le projet, ce qui implique une installation supplémentaire pour l'utilisateur.