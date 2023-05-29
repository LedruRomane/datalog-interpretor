import Edb
import Idb
import Predicate

# Évaluation du programme Datalog complet, boucle sur les IDB.
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
    print(evaluated_rules)


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

