# Projet Developing a Datalog Engine Extension for aggregate functions.

Projet développé par LEDRU Romane P2105081

## Installation

> ATTENTION REQUIREMENTS : **python3 et pandas** sont nécéssaires pour le lancement de ce projet.
Sur MacOS :
```bash 
brew install python3
pip3 install pandas
    
```


Sur Debian/Ubuntu like : 
```bash 
$ sudo apt-get update
$ sudo apt-get install python3
$ sudo pip3 install pandas
    
```


1.  Vous trouverez à la racine les fichiers .py du programme ainsi que le **main.py**, ouvrez un terminal à cet emplacement afin de lancez celui-ci.
2. Le programme demande un fichier datalog en entrée. Les fichiers de tests se trouvent dans **./tests**
3. Pour tester le programme il vous faudra lancer cette commande : 

```bash 
python3 main.py -f tests/NomduFichier.dl
```

L'extention .dl des fichiers correspond à un fichier datalog.

NOTE : LA PREMIERE EXECUTION EST GENERALEMENT PLUS LONGUE.

---

## Datalog disponibles

Différents datalog ont été préconcus en respectant le schéma (cf. rapport.pdf) pour tester directement le programme.
Rdv dans le dossier /tests pour y retrouver des datalogs plus ou moins exigents techniquement. Leur nom et les commentaires
dans les fichiers explicitent leur but.

>Ils sont directement utilisables avec la commande ci-dessus. Les résultats s'affichent dans un fichier généré ./output.txt
