import re

import pandas as pd

class Predicate:
    def __init__(self, predicate, params=[]):
        self.predicate = predicate
        self.params = params

    def getTitle(self):
        return self.predicate

    def filter(self, df):
        return False

    def print(self):
        print( f"Predicate ({type(self)}) name : ", self.predicate,"\nPredicate contents : ", self.params)

# Todo : Ajouter les classes qui héritent de Predicate pour les prédicats avec agrégation 
# et les prédicats de comparaison.
class AggregationPredicate(Predicate): # count, sum, avg, min, max.
    def __init__(self, predicate, params=[]):
        super().__init__(predicate, params)


class ComparisonPredicate(Predicate): # >=, >, <=, <, =\=, =:= .
    def __init__(self, predicate, params=[]):
        super().__init__(predicate, params)

    def filter(self, df):
        resultDf = df.copy()
        isStatic = False
        rotated = False
        Val1, Val2 = self.params[0], self.params[2]
        predicate = self.predicate
        if (self.isStatic(Val1) | self.isStatic(Val2)):
            isStatic = True
        if (self.isStatic(Val1)):
            rotated = True
            Val1, Val2 = Val2, Val1
        Column1 = Val1
        Column2 = Val2

        Column1 = Val1 if (Val1 in resultDf.columns) else f"#{Val1}#"
        if not (isStatic):
            Column2 = Val2 if (Val2 in resultDf.columns) else f"#{Val2}#"

        # if rotated
        if (rotated):
            if (predicate == "<"):
                predicate = ">"
            elif (predicate == ">"):
                predicate = "<"
            elif (predicate == "=<"):
                predicate = ">="
            elif (predicate == ">="):
                predicate = "=<"

        if (predicate == "=:="):
            if (isStatic):
                # filter the dataframe columns that match with the static variable
                resultDf = resultDf[resultDf[Column1] == Column2]
            else:
                # filter the dataframe columns that match with the variable
                resultDf = resultDf[resultDf[Column1] == resultDf[Column2]]

        elif (predicate == "=\="):
            if (isStatic):
                resultDf = resultDf[resultDf[Column1] != Column2]
            else:
                resultDf = resultDf[resultDf[Column1] != resultDf[Column2]]

        else:
            resultDf = self.filterNumeric(resultDf, predicate, Column1, Column2, isStatic)

        return resultDf
    
    def filterNumeric(self, df, predicate, column1, column2, isStatic = False):
        # Making sure that column are either int or float
        df[column1] = pd.to_numeric(df[column1], errors='coerce')
        if (isStatic):
            column2 = float(column2)
        else:
            df[column2] = pd.to_numeric(df[column2], errors='coerce')

        if (predicate == "<"):
            if (isStatic):
                df = df[df[column1] < column2]
            else:
                df = df[df[column1] < df[column2]]

        if (predicate == ">"):
            if (isStatic):
                df = df[df[column1] > column2]
            else:
                df = df[df[column1] > df[column2]]

        if (predicate == "=<"):
            if (isStatic):
                df = df[df[column1] <= column2]
            else:
                df = df[df[column1] <= df[column2]]

        if (predicate == ">="):
            if (isStatic):
                df = df[df[column1] >= column2]
            else:
                df = df[df[column1] >= df[column2]]

        return df
    
    def isStatic(self, variable):
        return not not (re.match(r"^(?:[\"']\w+[\"']|[0-9.]+)+$", str(variable).strip()))
        
class AtomicPredicate(Predicate): # edb like, etc.
    def __init__(self, predicate, params=[]):
        super().__init__(predicate, params)
    
    def filter(self, df, head_variables=[]):
        resultDf = df.copy()
        resultDf.columns = [f"#{str(param).strip()}#" if str(param).strip() not in head_variables else f"{str(param).strip()}" for i, param in enumerate(self.params)]

        # Static filter on columns that match with static variables in the body
        for i, param in enumerate(self.params):
            if not (re.match(r"^[a-z0-9]+$", str(param).strip())):
                continue
            # Filter rows from column i that do not match with the value of param
            resultDf = resultDf[resultDf.iloc[:, i] == param]
                
        # Remove underscore columns
        resultDf = resultDf.loc[:, ~resultDf.columns.str.contains('#_#')]
        return resultDf