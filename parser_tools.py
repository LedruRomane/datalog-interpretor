import re
import Idb
import Edb
import Predicate
import pandas as pd

# Extract EDB and IDB from a datalog program from a file.
def parse_input_file(file_path):
    edb_facts = []
    idb_rules = []

    with open(file_path, 'r') as file:
        lines = file.readlines()

        for line in lines:
            line = line.strip()

            # Comments and empty lines.
            if re.match(r"^(?:%.*|)$", line):
                continue

            # Part EDB
            if (re.match(r'^[A-Z]', line) and ':-' not in line ):
                # Divide the line into relation name and parameters.
                parts = re.split(r'\s*\(\s*|\s*,\s*|\s*\)\s*', line)
                relation = parts[0]
                params = parts[1:][:-1] # Remove empty elements.

                # Parse params to int or string
                parse_array(params)

                # Create an EDB object and add it to the list.
                edb_facts.append(Edb.EDB(relation, params))
            
            # Part IDB
            else:
                # Divide the line into head and body.
                parts = re.split(r'\s*:-\s*', line)
                head = parts[0]
                body = parts[1:]
                
                # Divide the head into relation name and parameters.
                parts = re.split(r'\s*\(\s*|\s*,\s*|\s*\)\s*', head)
                nameIDB = parts[0]
                params = parts[1:][:-1]
                predicates = []

                # Parsing Atomic Predicates (EDB like).
                predicateAtomicArray = re.findall(r'(\w+?\(.+?\)),?', body[0])
                predicatesAtomic = [predicate for predicate in predicateAtomicArray if predicate != '']
                for i in range(len(predicatesAtomic)):
                    predicatesAtomic[i] = predicatesAtomic[i].strip()
                    p = re.split(r'\s*\(\s*|\s*,\s*|\s*\)\s*', predicatesAtomic[i])
                    nameP = p[0]
                    paramsP = p[1:][:-1]
                    parse_array(paramsP)
                    predicatesAtomic[i] = Predicate.AtomicPredicate(nameP, paramsP)
                predicates.extend(predicatesAtomic)

                
                # Parsing Comparison predicates (E1 > E2 for exemple).
                predicateComparisonArray = re.findall(r'(["\']{0,1}(?:[a-zA-Z]\w+|[+-]?(?:[0-9]*[.])?[0-9]+)["\']{0,1}\s*(?:<|=<|>|>=|==|=:=|=\\=)\s*["\']{0,1}(?:[a-zA-Z]\w+|[+-]?(?:[0-9]*[.])?[0-9]+)["\']{0,1}),?', body[0])
                predicatesComparison = [predicate for predicate in predicateComparisonArray if predicate != '']
                for i in range(len(predicatesComparison)):
                    predicatesComparison[i] = predicatesComparison[i].strip()
                    p = re.split(r'(["\']{0,1}(?:[a-zA-Z]\w+|[+-]?(?:[0-9]*[.])?[0-9]+)["\']{0,1})\s*(<|=<|>|>=|==|=:=|=\\=)\s*(["\']{0,1}(?:[a-zA-Z]\w+|[+-]?(?:[0-9]*[.])?[0-9]+)["\']{0,1})', predicatesComparison[i])
                    p = [x for x in p if x != '']
                    parse_array(p)
                    predicatesComparison[i] = Predicate.ComparisonPredicate(p[1], p)
                predicates.extend(predicatesComparison)

                # Parsing Aggregate predicates (sum(E1) for exemple).



                idb_rules.append(Idb.IDB(nameIDB, params, predicates))
    return edb_facts, idb_rules

# Parser params to int or string
def parse_array(params):
    for i in range(len(params)):
                    if (re.match(r'^[0-9]+$', params[i])):
                        params[i] = int(params[i])
                    else:
                        params[i] = params[i].strip("'")

# cf. Step 1 eval: Parse edb into dataframe.
def parse_edb_dataframe(edb_facts):
    data_dict = {}
    data = []
    # Prepare data for dataframe.
    for edb in edb_facts:
        data.append(
            {
                'edb': edb.getEDBName(),
                'params': edb.getParams()
            }
        )

    # Build a table that merges tuples of the same relation.
    for fact in data:
        edb = fact['edb']
        params = fact['params']

        if edb not in data_dict:
            data_dict[edb] = []
        
        data_dict[edb].append(params)

    # Build a dataframe for each relation.
    dfs = {}
    for edb, values in data_dict.items():
        columns = [f'col{i}' for i in range(len(values[0]))]
        dfs[edb] = pd.DataFrame(values, columns=columns)

    return dfs # Return dict of dataframe with tables built.