class EDB:
    # edb: string (nom de la relation)
    # params: list (liste des données du tuple)
    #
    def __init__(self, edb="", params=[]):
        self.edb = edb
        self.params = params


    # Assesseurs
    def getEDBName(self):
        return self.edb
    
    def getNumParams(self):
        return len(self.params)
    
    def getParams(self):
        return self.params

    # Affichage
    def print(self):
        print( "EDB name : ", self.edb, "\nEDB contents : ", self.params, "\n--------")

