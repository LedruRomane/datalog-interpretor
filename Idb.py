import Predicate

class IDB:
    # idb: string (nom de la relation)
    # paramsHead: list (liste des paramètres de la tête)
    # body: list of Predicate (liste des prédicats présents dans le corps)
    def __init__(self, idb="", paramsHead=[], body=[]):
        self.idb = idb
        self.paramsHead = paramsHead
        self.body = body

    def getIDBName(self):
        return self.idb

    # Affichage
    def print(self):
        print( "\n------", self.idb ,"--------")
        print( "\nIDB Content Head : ", self.paramsHead)
        print( "IDB Content Body : ")
        for predicate in self.body:
            Predicate.Predicate.print(predicate)