import sys
import Edb
import Idb
from parse_input_file import parse_input_file
from Tools import importFile
import evaluation_program

# Main program pour notre Evaluateur de Datalog
def main():
    file = importFile()
    edb_facts, idb_rules = parse_input_file(file)

    # Afficher les relations EDB
    print ("\n----------------- EDB -------------------")
    for tuple in edb_facts:
        Edb.EDB.print(tuple)
    # Afficher les règles IDB
    print ("\n----------------- IDB -------------------")
    for rule in idb_rules:
        Idb.IDB.print(rule)

    # Évaluation
    evaluation_program.evaluate(edb_facts, idb_rules)

main()
