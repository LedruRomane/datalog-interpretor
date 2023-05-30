class EDB:
    # edb: string (relation's name)
    # params: list (tuple's data list)
    #
    def __init__(self, edb="", params=[]):
        self.edb = edb
        self.params = params

    def __str__(self):
        return str(self.edb + "(" + ", ".join(map(str, self.params)) + ")")

    # Accessors
    def getEDBName(self):
        return self.edb
    
    def getNumParams(self):
        return len(self.params)
    
    def getParams(self):
        return self.params

    # Console print
    def print(self):
        print( "EDB name : ", self.edb, "\nEDB contents : ", self.params, "\n--------")

