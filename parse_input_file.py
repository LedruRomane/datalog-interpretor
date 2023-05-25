import re

# Extrait les EDB et les IDB d'un datalog programme à partir d'un fichier
def parse_input_file(file_path):
    edb_facts = []
    idb_rules = []

    with open(file_path, 'r') as file:
        lines = file.readlines()

        for line in lines:
            line = line.strip()

            # Partie $EDB
            if (re.match(r'^[A-Z]', line) and ':-' not in line ):
                edb_facts.append(line)
            else:
                # Diviser la ligne en tête et corps des règles IDB
                parts = re.split(r'\s*->\s*|:-', line)
                head = parts[0].strip()
                body = parts[1].strip()

                # Récupérer le prédicat de la tête
                head_predicate = re.match(r'^[A-Z][a-zA-Z0-9_]*', head).group()

                # Récupérer les prédicats du corps
                body_predicates = body

                idb_rules.append((head_predicate, body_predicates))

    return edb_facts, idb_rules

# Charger un datalog progamme à partir d'un fichier
edb_facts, idb_rules = parse_input_file('bdd.dl')

# Afficher les relations EDB
print("EDB Relations:")
for relation in edb_facts:
    print(relation)

# Afficher les règles IDB
print("\nIDB Rules:")
for head, body in idb_rules:
    print("Head Predicate:", head)
    print("Body Predicates:", body)
    print()
