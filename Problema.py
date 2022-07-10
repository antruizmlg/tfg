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
                id = 's' + str(i) + str(j)
                self.tablero[i][j] = Estado(id)

        self.filaFinal = self.generador_aleatorio(numFilas - 1)
        self.columnaFinal = self.generador_aleatorio(numColumnas - 1)

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

    def generar_Problema(self):
        listaNodos = {}
        listaHiperaristas = []
        for i in range(len(self.tablero)):
            for j in range(len(self.tablero[i])):
                listaNodos[self.tablero[i][j].id] = self.tablero[i][j]
                for a in self.acciones.keys():
                    listaHiperaristas.append(Hiperarista(self.tablero[i][j], self.getProbabilidades(i, j, a), a, self.acciones[a]))
        hg = Hipergrafo(listaNodos, listaHiperaristas)
        politica, heuristico = self.get_politica_heuristico()
        return hg, self.tablero[self.filaInicial][self.columnaInicial], heuristico, politica

    def getProbabilidades(self, fila, columna, accion):
        dicEstados = {}
        probabilidades = {}
        for a in self.acciones.keys():
            dicEstados[a] = self.sucesor_accion(fila, columna, a)
            probabilidades[dicEstados[a].id] = 0
        
        for a in self.acciones.keys():
            probabilidades[dicEstados[a].id] += self.get_probabilidad_por_transicion(accion, a)

        return probabilidades

    def informacion(self):   
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

    def sucesor_accion(self, fila, columna, accion):
        if accion == 'ARRIBA':
            if fila - 1 < 0:
                return self.tablero[fila][columna]
            else:
                return self.tablero[fila-1][columna]
        if accion == 'IZQUIERDA':
            if columna - 1 < 0:
                return self.tablero[fila][columna]
            else:
                return self.tablero[columna - 1][columna]
        if accion == 'DERECHA':
            if columna + 1 >= len(self.tablero[0]):
                return self.tablero[fila][columna]
            else:
                return self.tablero[fila][columna+1]    
        if accion == 'ABAJO':
            if fila + 1 >= len(self.tablero):
                return self.tablero[fila][columna]
            else:
                return self.tablero[fila+1][columna]

    def get_politica_heuristico(self):
        politica = {}
        heuristico = {}
        for i in range(len(self.tablero)):
            for j in range(len(self.tablero[i])):
                politica[self.tablero[i][j].id] = 'ARRIBA' # POLITICA ARBITRARIA
                heuristico[self.tablero[i][j].id] = self.tablero[i][j].h()
        return Politica(politica), FuncionDeValor(heuristico)

    @staticmethod
    def generador_aleatorio(numero):
        if random.randint(0, 1) == 0:
            return 0
        else:
            return numero