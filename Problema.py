from Estado import *
import random

class Problema:
    def __init__(self, numFilas, numColumnas, numSumideros, probabilidades):
        for i in range(numFilas):
            for j in range(numColumnas):
                id = 's' + i + j
                self.tablero[i][j] = Estado(id)

        filaFinal = self.generador_aleatorio(numFilas - 1)
        columnaFinal = self.generador_aleatorio(numColumnas - 1)

        self.tablero[filaFinal][columnaFinal].setTerminal()

        i = 0
        while i < numSumideros:
            numFila = random.randint(0, numFilas)
            numCol = random.randint(0, numColumnas)
            if not self.tablero[numFila][numCol].terminal:
                self.tablero[numFila][numCol].setSumidero()
                i += 1

        self.filaInicial = numFilas // 2
        self.columnaInicial = numColumnas // 2
        self.probabilidades = probabilidades

    def generar_Problema(self):
        

    @staticmethod
    def generador_aleatorio(numero):
        if random.randint(0, 1) == 0:
            return 0
        else:
            return numero