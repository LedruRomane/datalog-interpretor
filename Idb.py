import Predicate

class IDB:
    # idb: string (relation's name)
    # paramsHead: list (head's parameters)
    # body: list of Predicate (body's content)
    def __init__(self, idb="", paramsHead=[], body=[]):
        self.idb = idb
        self.paramsHead = paramsHead
        self.body = body

    def __str__(self):
        return str(self.idb + "(" + ", ".join(self.paramsHead) + ") :- " + ", ".join(map(str, self.body)))

    # Acessors
    def getIDBName(self):
        return self.idb

    # Print into console.
    def print(self):
        print( "\n------", self.idb ,"--------")
        print( "\nIDB Content Head : ", self.paramsHead)
        print( "IDB Content Body : ")
        for predicate in self.body:
            Predicate.Predicate.print(predicate)