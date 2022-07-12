from Estado import *
from Hiperarista import *
from Hipergrafo import *
from Politica import *
from FuncionDeValor import *
import random

class Problema:
    def __init__(self, numFilas, numColumnas, numSumideros, probabilidades):

        self.tablero = [[0 for j in range(numColumnas)] for i in range(numFilas)]

        for i in range(numFilas):
            for j in range(numColumnas):
                id = 's' + str(i) + "_" + str(j)
                self.tablero[i][j] = Estado(id)

        self.filaFinal = self.generador_posicion_final(numFilas - 1)
        self.columnaFinal = self.generador_posicion_final(numColumnas - 1)

        self.tablero[self.filaFinal][self.columnaFinal].setTerminal()

        self.sumideros = []

        i = 0
        while i < numSumideros:
            numFila = random.randint(0, numFilas - 1)
            numCol = random.randint(0, numColumnas - 1)
            if not self.tablero[numFila][numCol].terminal:
                self.tablero[numFila][numCol].setSumidero()
                i += 1
                self.sumideros.append("["+str(numFila)+", "+str(numCol)+"]")

        self.acciones = {'ARRIBA': 0.8, 'DERECHA': 0.6, 'IZQUIERDA': 0.6, 'ABAJO': 0.4}
        self.filaInicial = numFilas // 2
        self.columnaInicial = numColumnas // 2
        self.probabilidades = probabilidades

    def generar_problema(self):
        estado_por_id = {}
        estados_hg = {}
        ha_list = []
        for i in range(len(self.tablero)):
            for j in range(len(self.tablero[i])):
                state = self.tablero[i][j]
                estado_por_id[state.id] = state
                for a in self.acciones.keys():
                    ha_list.append(Hiperarista(self.get_probs(i, j, a), a, self.acciones[a]))
                estados_hg[state.id] = ha_list
                ha_list = []
        hg = Hipergrafo(estados_hg)
        politica, heuristico = self.get_politica_y_heuristico()
        return estado_por_id, hg, self.tablero[self.filaInicial][self.columnaInicial], heuristico, politica

    def get_probs(self, fila, columna, accion):
        sucesores = self.get_sucesores(fila, columna)
        probabilidades = {}
        
        for suc in sucesores.values():
            probabilidades[suc.id] = 0
        
        for a in self.acciones.keys():
            probabilidades[sucesores[a].id] += self.get_probabilidad_por_transicion(accion, a)

        return probabilidades

    def print_info(self):   
        print("Tamaño de tablero: " + str(len(self.tablero)) + "x" + str(len(self.tablero[0])))
        for s in self.sumideros:
                print("Sumidero: "+ s)
        print("Celda inicial: [" + str(self.filaInicial) + ", " + str(self.columnaInicial) + "]")
        print("Celda objetivo: [" + str(self.filaFinal) + ", " + str(self.columnaFinal) + "]\n")
        
    def get_probabilidad_por_transicion(self, a1, a2):
        if a1 == 'ARRIBA' and a2 == 'ARRIBA':
            return self.probabilidades[0][0]
        if a1 == 'ARRIBA' and a2 == 'DERECHA':
            return self.probabilidades[0][1]
        if a1 == 'ARRIBA' and a2 == 'IZQUIERDA':
            return self.probabilidades[0][2]            
        if a1 == 'ARRIBA' and a2 == 'ABAJO':
            return self.probabilidades[0][3]
        if a1 == 'DERECHA' and a2 == 'ARRIBA':
            return self.probabilidades[1][0]
        if a1 == 'DERECHA' and a2 == 'DERECHA':
            return self.probabilidades[1][1]
        if a1 == 'DERECHA' and a2 == 'IZQUIERDA':
            return self.probabilidades[1][2]
        if a1 == 'DERECHA' and a2 == 'ABAJO':
            return self.probabilidades[1][3]
        if a1 == 'IZQUIERDA' and a2 == 'ARRIBA':
            return self.probabilidades[2][0]
        if a1 == 'IZQUIERDA' and a2 == 'DERECHA':
            return self.probabilidades[2][1]
        if a1 == 'IZQUIERDA' and a2 == 'IZQUIERDA':
            return self.probabilidades[2][2]
        if a1 == 'IZQUIERDA' and a2 == 'ABAJO':
            return self.probabilidades[2][3]
        if a1 == 'ABAJO' and a2 == 'ARRIBA':
            return self.probabilidades[3][0]
        if a1 == 'ABAJO' and a2 == 'DERECHA':
            return self.probabilidades[3][1]
        if a1 == 'ABAJO' and a2 == 'IZQUIERDA':
            return self.probabilidades[3][2]
        if a1 == 'ABAJO' and a2 == 'ABAJO':
            return self.probabilidades[3][3]

    def get_sucesores(self, fila, columna):
        sucesores = {}
        if fila - 1 >= 0:
            sucesores['ARRIBA'] = self.tablero[fila-1][columna]
        else:
            sucesores['ARRIBA'] = self.tablero[fila][columna]
        if fila + 1 < len(self.tablero):
            sucesores['ABAJO'] = self.tablero[fila+1][columna]
        else:
            sucesores['ABAJO'] = self.tablero[fila][columna]
        if columna - 1 >= 0:
            sucesores['IZQUIERDA'] = self.tablero[fila][columna-1]
        else:
            sucesores['IZQUIERDA'] = self.tablero[fila][columna]
        if columna + 1 < len(self.tablero[0]):
            sucesores['DERECHA'] = self.tablero[fila][columna+1]
        else:
            sucesores['DERECHA'] = self.tablero[fila][columna]
        return sucesores

    def get_politica_y_heuristico(self):
        politica = {}
        heuristico = {}
        for i in range(len(self.tablero)):
            for j in range(len(self.tablero[i])):
                state = self.tablero[i][j]
                politica[state.id] = None
                heuristico[state.id] = state.h()
        return Politica(politica), FuncionDeValor(heuristico)

    @staticmethod
    def generador_posicion_final(p):
        if random.randint(0, 1) == 0:
            return 0
        else:
            return p