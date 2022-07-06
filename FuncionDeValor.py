class FuncionDeValor:    
    def __init__(self, dictValores):
        self.dv = dictValores

    def setValor(self, estado, nuevoValor):
        self.dv[estado.id] = nuevoValor

    def getValor(self, estado):
        return self.dv[estado.id]