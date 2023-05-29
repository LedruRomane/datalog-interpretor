class Predicate:
    def __init__(self, predicate, params=[]):
        self.predicate = predicate
        self.params = params

    def print(self):
        print( "Predicate name : ", self.predicate, "\nPredicate contents : ", self.params)
    