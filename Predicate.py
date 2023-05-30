import re

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
class AggregationPredicate(Predicate): # count, sum, avg, etc.
    def __init__(self, predicate, params=[]):
        super().__init__(predicate, params)


class ComparisonPredicate(Predicate): # > < \= etc.
    def __init__(self, predicate, params=[]):
        super().__init__(predicate, params)

        
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