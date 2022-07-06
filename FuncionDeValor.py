class FuncionDeValor:    
    def __init__(self, dictValores):
        self.dv = dictValores

    def setValor(self, estado, nuevoValor):
        self.dv[estado] = nuevoValor

    def getValor(self, estado):
        return self.dv[estado]