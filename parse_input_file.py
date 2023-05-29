import re
import Idb
import Edb
import Predicate
import Tools

# Extrait les EDB et les IDB d'un datalog programme à partir d'un fichier
def parse_input_file(file_path):
    edb_facts = []
    idb_rules = []

    with open(file_path, 'r') as file:
        lines = file.readlines()

        for line in lines:
            line = line.strip()

            # Partie EDB
            if (re.match(r'^[A-Z]', line) and ':-' not in line ):
                # Diviser la ligne en nom de la relation et paramètres
                parts = re.split(r'\s*\(\s*|\s*,\s*|\s*\)\s*', line)
                relation = parts[0]
                params = parts[1:][:-1] # Enlever le dernier élément qui est vide.

                # Parser les paramètres en entiers ou en chaînes de caractères
                Tools.parser_array(params)

                # Créer un objet EDB et l'ajouter à la liste
                edb_facts.append(Edb.EDB(relation, params))
            
            # Partie IDB
            else:
                # Diviser la ligne en tête et corps
                parts = re.split(r'\s*:-\s*', line)
                head = parts[0]
                body = parts[1:]
                
                # Diviser la tête en nom de la relation et paramètres
                parts = re.split(r'\s*\(\s*|\s*,\s*|\s*\)\s*', head)
                nameIDB = parts[0]
                params = parts[1:][:-1]

                # Parser le body en liste de prédicats
                predicateArray = re.split(r'(\w+?\(.+?\)),?', body[0])
                predicates = [predicate for predicate in predicateArray if predicate != '']
                for i in range(len(predicates)):
                    predicates[i] = predicates[i].strip()
                    p = re.split(r'\s*\(\s*|\s*,\s*|\s*\)\s*', predicates[i])
                    nameP = p[0]
                    paramsP = p[1:][:-1]
                    Tools.parser_array(paramsP)
                    predicates[i] = Predicate.Predicate(nameP, paramsP)

                idb_rules.append(Idb.IDB(nameIDB, params, predicates))


    return edb_facts, idb_rules
