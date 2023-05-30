import sys
import Edb
import Idb
from parser_tools import parse_input_file, parse_to_output
from files_tools import importFile, exportFile
import evaluation_program

def main():
    file = importFile()
    edb_facts, idb_rules = parse_input_file(file)

    # Print into console EDB parsed.
    print ("\n----------------- EDB -------------------")
    for tuple in edb_facts:
        Edb.EDB.print(tuple)
    # Print into console IDB parsed.
    print ("\n----------------- IDB -------------------")
    for rule in idb_rules:
        Idb.IDB.print(rule)

    # Evaluate
    evalFact = evaluation_program.evaluate(edb_facts, idb_rules)

    #todo: load results into a file
    output = parse_to_output(edb_facts, idb_rules, evalFact)
    exportFile("output.txt", output)

main()
