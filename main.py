# Relations EDB
edb_facts = [
    ['Actor', '344759', 'Douglas', 'Fowley'],
    ['Casts', '344759', '29851'],
    ['Casts', '355713', '29000'],
    ['Movie', '7909', 'A Night in Armour', '1910'],
    ['Movie', '29000', 'Arizona', '1940'],
    ['Movie', '29445', 'Ave Maria', '1940']
]

# Règles IDB
idb_rules = [
    (['Q1', 'y'], [['Movie', 'x', 'y', '1940']]),
    ]

# Fonction d'évaluation
def evaluate(edb_facts, idb_rules):
    evaluated_rules = []

    for rule in idb_rules:
        head = rule[0]
        body = rule[1:]
        result = evaluate_rule(head, body, edb_facts)
        evaluated_rules.append((head, result))

    return evaluated_rules


def evaluate_rule(head, body, edb_facts):
    result = []

    for relation in edb_facts:
        if match_atom(relation, body[0][0]):
            arguments = get_arguments(relation, head[1:], body[0][0])
            if arguments not in result:  # Ajout de cette condition pour éviter les doublons
                result.append(arguments)
    return result


def match_atom(relation, atom):
    is_match = []
    if relation[0] != atom[0] or len(relation) != len(atom):
        return False

    for i in range(1, len(relation)):
        is_match.append(relation[i] == atom[i])
    
    return True in is_match

def get_arguments(relation, head_arguments, body):
    arguments = []
    print('relation: ', relation)
    print('head: ', head_arguments)
    print('body: ', body)
    for i in range(len(head_arguments)):
        for j in range(len(body)):
            if head_arguments[i] == body[j]:
                arguments.append(relation[j])
    
    return arguments


# Évaluation
evaluated_rules = evaluate(edb_facts, idb_rules)

# Affichage des résultats
for rule in evaluated_rules:
    head = rule[0]
    results = rule[1]
    print("Head:", head)
    print("Results:")
    for result in results:
        print(result)
    print()
