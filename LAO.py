from Hipergrafo import *

class LAO:
    def __init__(self, hipergrafo, estadoInicial, heuristico):
        self.hipergrafo = hipergrafo
        self.eIni = estadoInicial
        self.heuristico = heuristico

    def LAO(self):
        V = self.heuristico
        F = [self.eIni]
        I = []
        G = Hipergrafo([self.eIni], None)
        GV = Hipergrafo([self.eIni], None)
