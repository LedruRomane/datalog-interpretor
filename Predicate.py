import re

import pandas as pd

class Predicate:
    def __init__(self, predicate, params=[]):
        self.predicate = predicate
        self.params = params

    def getTitle(self):
        return self.predicate

    def eval(self, df):
        return False

    def print(self):
        print( f"Predicate ({type(self)}) name : ", self.predicate,"\nPredicate contents : ", self.params)

# Todo : Ajouter les classes qui héritent de Predicate pour les prédicats avec agrégation 
# et les prédicats de comparaison.
class AggregationPredicate(Predicate): # count, sum, avg, min, max.
    def __init__(self, predicate, params=[]):
        super().__init__(predicate, params)

    def parseColumn(self, df, head_variables=[]):
        columnGroup = self.params[:-2]
        column = self.params[-2]
        outputColumn = self.params[-1]

        column = column if (column in head_variables) else f"#{column}#"
        outputColumn = outputColumn if (outputColumn in head_variables) else f"#{outputColumn}#"
        for i, param in enumerate(columnGroup):
            columnGroup[i] = param if (param in head_variables) else f"#{param}#"

        return columnGroup, column, outputColumn

    def eval(self, df, head_variables=[]):
        resultDf = df.copy()

        columnGroup, column, outputColumn = self.parseColumn(resultDf, head_variables)
        
        # TODO: Verify behaviour of the following predicates
        if self.predicate == 'Count':
            # Count the number of rows in the dataframe
            resultDf = self.evalPredicate(resultDf, len, columnGroup, column, outputColumn)
        elif self.predicate == 'Min':
            # Get the single minimum value for Column variable, ignoring nulls
            resultDf = self.evalPredicate(resultDf, pd.DataFrame.min, columnGroup, column, outputColumn)
        elif self.predicate == 'Max':
            # Get the single maximum value for Column variable, ignoring nulls
            resultDf = self.evalPredicate(resultDf, pd.DataFrame.max, columnGroup, column, outputColumn)
        elif self.predicate == 'Sum':
            # Get the sum of the values for Column variable, ignoring nulls
            resultDf = self.evalPredicate(resultDf, pd.DataFrame.sum, columnGroup, column, outputColumn)
        elif self.predicate == 'Avg':
            # Get the average of the values for Column variable, ignoring nulls without groupby
            resultDf = self.evalPredicate(resultDf, pd.DataFrame.mean, columnGroup, column, outputColumn)

        return resultDf
    
    def evalPredicate(self, df, function, columnGroup, column, outputColumn):
        if (len(columnGroup) > 0):
            evalDf = df.groupby(columnGroup)[column].apply(function).reset_index(name=outputColumn)
            df = pd.merge(df, evalDf, on=columnGroup, how='left')
        else:
            if (function == len):
                # Count the number of rows in the dataframe
                evalDf = df[column].apply(function)
            elif (function == pd.DataFrame.min):
                evalDf = df[column].min()
            elif (function == pd.DataFrame.max):
                evalDf = df[column].max()
            elif (function == pd.DataFrame.sum):
                evalDf = df[column].sum()
            elif (function == pd.DataFrame.mean):
                evalDf = df[column].mean()

            df = df.assign(**{outputColumn: evalDf})
        return df

class ComparisonPredicate(Predicate): # >=, >, <=, <, =\=, =:= .
    def __init__(self, predicate, params=[]):
        super().__init__(predicate, params)

    def eval(self, df):
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
    
    def eval(self, df, head_variables=[]):
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