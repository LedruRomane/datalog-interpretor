# Projet Developing a Datalog Engine Extension for aggregate functions.

Projet développé par LEDRU Romane P2105081

## Installation

> ATTENTION **Python3** sera nécessaire au lancement et au test de ce projet. 

1. Dans le répertoire /Prog vous y trouverez les fichiers .py du programme ainsi que le main, ouvrez un terminal à cet emplacement afin de lancez celui-ci.
2. Le programme demande un fichier datalog en entrée. Les fichiers de tests se trouvent dans ./tests
3. Pour tester le programme il vous faudra lancer une commande du type : 

```bash 
python3 main.py -i tests/NomduFichier.dl
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
>       Les EDB listés, terminant par un point.
> 
>       Les IDB listés terminant par un point, avec :- dans sa définition.
>
> 3 - Les prédicats commencent tous par une majuscule et sont séparés d'une virgule seulement.

### 2- Parsing : 

**parse_input_file.py** permet de prendre en entrée le fichier et itérer sur chacune de ses lignes afin d'en extraire les EDB d'un côté, et les IDB split avec la Head et le Body de l'autre.

C'est grâce à nos règles imposées plus haut qu'il nous est aisé de split correctement les EDB (leur nom et leur contenu) et les IDB (leur head et leur body).

Il retourne donc un tableau contenant un tableau d'EDB et un tableau d'IDB. 

---


## Partie 2 : Evaluation

On va donner à un programme d'évaluation notre tableau retourné par parse_input_file afin de retourner le resultat dans un fichier. 

Pour ce faire on va créer un fichier **evaluation_progam.py** qui prendra en entrée les données retournées de notre parser.