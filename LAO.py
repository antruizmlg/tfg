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
        s = self.hipergrafo.interseccion(F).obtenerEstadoNoTerminal()
        while s is not None:
            F.remove(s) # Eliminamos el estado s
            for estado in self.hipergrafo.sucesores(s): # Por cada sucesor de s en el hipergrafo
                if estado not in I: # Si el sucesor no se encuentra en el conjunto I
                    F.append(estado) # Lo introducimos en el conjunto F
            I.append(s) # Introducimos s en el conjunto I