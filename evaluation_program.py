import Edb
import Idb
import Predicate
import pandas as pd

# Évaluation du programme Datalog complet, boucle sur les IDBs à évaluer.
def evaluate(edb_facts, idb_rules):
    evaluated_rules = []
    for rule in idb_rules:
        head = rule.paramsHead
        body = rule.body
        predicates = []
        for predicate in body:
            predicates.append(predicate)
        result = evaluate_rule(head, predicates, edb_facts)
        evaluated_rules.append(result)

    print_evaluator()
    dataframe_edb_parser(edb_facts)

# Etape 1 : Parser des edb dans un dataframe.
def dataframe_edb_parser(edb_facts):
    data_dict = {}
    data = []
    for edb in edb_facts:
        data.append(
            {
                'edb': edb.getEDBName(),
                'params': edb.getParams()
            }
        )

    for items in data:
        edb = items['edb']
        params = items['params']

        if edb not in data_dict:
            data_dict[edb] = []
        
        data_dict[edb].append(params)

    dfs = {}
    for edb, values in data_dict.items():
        columns = [f'col{i}' for i in range(len(values[0]))]
        dfs[edb] = pd.DataFrame(values, columns=columns)

    return dfs

def evaluate_rule(head, predicates, edb_facts):
    result = []

    # If there is a aggregation in the head

    # Else evaluate the rule normally

    return result
    


def match_atom(relation, atom):
    #todo: match atom 
    return True

def get_arguments(relation, head_arguments, body):
    arguments = []
    #todo: match arguments and return who is correct
    
    return arguments

def print_evaluator():
    print("\n----- Evaluation program ------\n")

