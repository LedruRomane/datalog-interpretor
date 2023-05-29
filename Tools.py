import re
import sys, argparse

def parser_array(params):
    for i in range(len(params)):
                    if (re.match(r'^[0-9]+$', params[i])):
                        params[i] = int(params[i])
                    else:
                        params[i] = params[i].strip("'")

def importFile():
   # Création d'un objet ArgumentParser
    parser = argparse.ArgumentParser()

    # Ajout des arguments souhaités
    parser.add_argument('-f', '--file', help='Fichier à analyser')

    # Analyse des arguments de ligne de commande
    args = parser.parse_args()

    return args.file