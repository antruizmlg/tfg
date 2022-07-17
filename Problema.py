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

        self.filaInicial = numFilas // 2
        self.columnaInicial = numColumnas // 2

        self.sumideros = []

        i = 0
        while i < numSumideros:
            numFila = random.randint(0, numFilas - 1)
            numCol = random.randint(0, numColumnas - 1)
            if not self.tablero[numFila][numCol].sumidero and not self.tablero[numFila][numCol].terminal and not (numFila == self.filaInicial and numCol == self.columnaInicial):
                self.tablero[numFila][numCol].setSumidero()
                i += 1
                self.sumideros.append("["+str(numFila)+", "+str(numCol)+"]")

        self.acciones = {'ARRIBA': 1, 'DERECHA': 1, 'IZQUIERDA': 1, 'ABAJO': 1}
        self.probabilidades = probabilidades

    def generar_problema(self):
        estado_por_id = {}
        estados_hg = {}
        ha_list = []
        sumidero_state = Estado('s_ss')
        sumidero_state.setTerminal()
        estado_por_id[sumidero_state.id] = sumidero_state
        for i in range(len(self.tablero)):
            for j in range(len(self.tablero[i])):
                state = self.tablero[i][j]
                estado_por_id[state.id] = state
                if not state.sumidero:
                    for a in self.acciones.keys():
                        ha_list.append(Hiperarista(self.get_probs(i, j, a), a, self.acciones[a]))
                else:
                    ha_list.append(Hiperarista({sumidero_state.id: 1}, 'ARRIBA', 30))
                estados_hg[state.id] = ha_list
                ha_list = []
        hg = Hipergrafo(estados_hg)
        politica, heuristico = self.get_p_and_h()
        return estado_por_id, hg, self.tablero[self.filaInicial][self.columnaInicial], heuristico, politica

    def get_probs(self, fila, columna, accion):
        sucesores = self.get_sucesores(fila, columna)
        probabilidades = {}
        probs_sol = {}
        
        for suc in sucesores.values():
            probabilidades[suc.id] = 0
        
        for a in self.acciones.keys():
            probabilidades[sucesores[a].id] += self.get_probabilidad_por_transicion(accion, a)

        for suc in probabilidades.keys():
            prob = probabilidades[suc]
            if prob > 0:
                probs_sol[suc] = prob # Si la probabilidad de alcanzar un estado desde otro estado es 0, no se considera como sucesor.

        return probs_sol

    def print_info(self):   
        print("Tamaño de tablero: " + str(len(self.tablero)) + "x" + str(len(self.tablero[0])))
        for s in self.sumideros:
                print("Sumidero: "+ s)
        print("Celda inicial: [" + str(self.filaInicial) + ", " + str(self.columnaInicial) + "]")
        print("Celda objetivo: [" + str(self.filaFinal) + ", " + str(self.columnaFinal) + "]\n")

    def print_tablero(self, p):
        print("------------------------------------------------------------------------")
        for i in range(len(self.tablero)):
            for j in range(len(self.tablero[0])):
                if self.tablero[i][j].terminal:
                    print('TT', end = ' ')
                elif self.tablero[i][j].sumidero:
                    print('SS', end = ' ')
                else:
                    if p.get_politica(self.tablero[i][j].id) == 'ARRIBA':
                        print('AR', end = ' ')
                    if p.get_politica(self.tablero[i][j].id) == 'DERECHA':
                        print('DE', end = ' ')
                    if p.get_politica(self.tablero[i][j].id) == 'IZQUIERDA':
                        print('IZ', end = ' ')
                    if p.get_politica(self.tablero[i][j].id) == 'ABAJO':
                        print('AB', end = ' ')
                    if p.get_politica(self.tablero[i][j].id) is None:
                        print('##', end = ' ')
            print("")
        print("------------------------------------------------------------------------")
        
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

    def get_p_and_h(self):
        politica = {}
        heuristico = {}
        for i in range(len(self.tablero)):
            for j in range(len(self.tablero[i])):
                state = self.tablero[i][j]
                politica[state.id] = None
                heuristico[state.id] = state.h()
        politica['s_ss'] = None
        heuristico['s_ss'] = 0
        return Politica(politica), FuncionDeValor(heuristico)

    @staticmethod
    def generador_posicion_final(p):
        if random.randint(0, 1) == 0:
            return 0
        else:
            return p