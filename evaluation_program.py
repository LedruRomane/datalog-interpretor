import re
from parser_tools import parse_edb_dataframe, create_fact
import Predicate
import pandas as pd

# Evaluate the whole Datalog program, loop on IDBs to evaluate and return them.
def evaluate(edb_facts, idb_rules):
    evaluated_rules = {}

    # Step 1 : Parse edb into dataframe (cf. README & parser_tools).
    dataframes = parse_edb_dataframe(edb_facts)

    # Loop on IDB rules.
    for rule in idb_rules:
        idbName = rule.getIDBName()
        head = rule.paramsHead
        body = rule.body

        if idbName not in evaluated_rules:
            evaluated_rules[idbName] = {
                'head': head,
                'rows': []
            }

        ruleResult = []
        ruleCount = 0

        # Step 2 : Evaluate an IDB rule until there is no more change in the result.
        ruleResult = evaluate_rule(head, body, dataframes)
        ruleCount = len(ruleResult)
        while ruleCount > 0:
            ruleCount = 0
            for row in ruleResult:
                # Save in dataframes the result of the rule evaluation.
                if idbName not in dataframes:
                    dataframes[idbName] = pd.DataFrame(columns=row.keys()) # Add to facts

                if ([*row.values()] not in dataframes[idbName].values.tolist()):
                    ruleCount += 1
                    dataframes[idbName].loc[len(dataframes[idbName])] = row
                    evaluated_rules[idbName]['rows'].extend([row])
            
            ruleResult = evaluate_rule(head, body, dataframes)

    

    print_evaluator(evaluated_rules)

    return evaluated_rules

# Step 2 : Evaluate an IDB rule.
def evaluate_rule(head, body, dataframes):
    result = []

    aggregateVariables = []
    postAggregateComparisonPredicates = []

    # Let's find all the aggregate variables in the body so we can ignore comparisons on them at first run.
    for predicate in body:
        if type(predicate) is Predicate.AggregationPredicate:
            var = predicate.params[-1].strip()
            aggregateVariables.append(var)

    # Step 2.1 : Evaluate all atomic predicates in the body.
    atomPredicateResults = [] # dFs of each Atomic predicate result
    for predicate in body:
        if type(predicate) is Predicate.AtomicPredicate:
           if predicate.getTitle() in dataframes:
                df = predicate.eval(dataframes[predicate.getTitle()], head)
                atomPredicateResults.append(df)

    if not atomPredicateResults:
        return result

    # Merge all atomic predicate results
    df = merge_dataframes(atomPredicateResults)


    # Step 2.2 : Evaluate all comparisons predicates in the body. (that does not contain Aggregate variables)
    for predicate in body:
        bypass = False
        if type(predicate) is Predicate.ComparisonPredicate:
            for var in aggregateVariables:
                if var in predicate.params:
                    postAggregateComparisonPredicates.append(predicate)
                    bypass = True
                    break
            if not bypass:
                df = predicate.eval(df)


    # Step 2.3 : Evaluate all aggregate predicates in the body.
    for predicate in body:
        if type(predicate) is Predicate.AggregationPredicate:
            df = predicate.eval(df, head)


    # Step 2.4 : Evaluate all comparisons predicates in the body. (that contains Aggregate variables)
    for predicate in postAggregateComparisonPredicates:
        df = predicate.eval(df)

    # Cleaning up the dataframe
    # Delete all #Y# columns generated by the AtomicPredicate.filter() method
    df = df.loc[:, ~df.columns.str.contains('#[a-zA-Z0-9]+#')]

    # Add the result to the list of results
   
    for _, row in df.iterrows():
        # Save the result as a dictionary
        result.append(row.to_dict())
    return result
    

def merge_dataframes(atomPredicateResults):
    if (len(atomPredicateResults) == 0):
        return None
    df = atomPredicateResults[0]
    for relDf in atomPredicateResults[1:]:
        df = pd.merge(df, relDf, how='cross')

    # filter rows for matching tokens
    tokens = df.columns.tolist()
    tokens = map(lambda x: x.split('_')[0], tokens)
    tokens = set(tokens)
    df = filterTable(df, tokens)
    
    return df

def filterTable(df, tokens): # This is definitely not the best way to do this
    # tokens are tags that column that contains them in their name must have the same value
    for token in tokens:
        columns = df.columns.tolist()
        columns = filter(lambda x: x.split('_')[0] == token, columns)
        columns = list(columns)
        if (len(columns) == 1):
            continue
        # filter rows where rows have the same value for all columns
        df = df[df[columns].apply(lambda x: len(set(x)) == 1, axis=1)]
        if (len(df) == 0):
            return df
        # keep only one column
        df = df.drop(columns=columns[1:])
        # rename column
        df = df.rename(columns={columns[0]: token})
    return df

def print_evaluator(rules):
    print("\n----- Evaluation program ------\n")
    for rule in rules:
        head, rows = rules[rule]['head'], rules[rule]['rows']
        for row in rows:
            print(f"{create_fact(rule, head, row)}")
        print("\n")

