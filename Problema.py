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

        self.acciones = {'NE': 1, 'N': 1, 'NO': 1, 'O': 1, 'SO': 1, 'S': 1, 'SE': 1, 'E': 1}
        self.probabilidades = probabilidades

    def generar_problema(self):
        estado_por_id = {}
        estados_hg = {}
        ha_list = []
        sumidero_state = Estado('s_ss')
        sumidero_state.setTerminal()
        estado_por_id[sumidero_state.id] = sumidero_state
        for i in range(len(self.tablero)):
            for j in range(len(self.tablero[0])):
                state = self.tablero[i][j]
                estado_por_id[state.id] = state
                if not state.sumidero:
                    for a in self.acciones.keys():
                        ha_list.append(Hiperarista(self.get_probs(i, j, a), a, self.acciones[a]))
                else:
                    ha_list.append(Hiperarista({sumidero_state.id: 1}, 'N', len(self.tablero)*3))
                estados_hg[state.id] = ha_list
                ha_list = []
        hg = Hipergrafo(estados_hg)
        politica, heuristico = self.get_p_and_h()
        return estado_por_id, hg, self.tablero[self.filaInicial][self.columnaInicial], heuristico, politica

    def get_probs(self, fila, columna, accion):
        probs = {}

        for a in self.probabilidades[accion].keys():
            suc = self.successor(fila, columna, a)
            if suc in probs.keys():
                probs[suc.id] += self.probabilidades[accion][a]
            else:
                probs[suc.id] = self.probabilidades[accion][a]
        return probs

    def successor(self, fila, columna, accion):
        if accion == 'N':
            return self.get_successor_state(fila, columna, fila - 1, columna)
        if accion == 'S':
            return self.get_successor_state(fila, columna, fila + 1, columna)
        if accion == 'E':
            return self.get_successor_state(fila, columna, fila, columna + 1)            
        if accion == 'O':
            return self.get_successor_state(fila, columna, fila, columna - 1)
        if accion == 'NE':
            return self.get_successor_state(fila, columna, fila - 1, columna + 1)
        if accion == 'NO':
            return self.get_successor_state(fila, columna, fila - 1, columna - 1)
        if accion == 'SE':
            return self.get_successor_state(fila, columna, fila + 1, columna + 1)
        if accion == 'SO':
            return self.get_successor_state(fila, columna, fila + 1, columna - 1)

    def get_successor_state(self, of, oc, nf, nc):
        if nf >= 0 and nf < len(self.tablero) and nc >= 0 and nc < len(self.tablero[0]):
            return self.tablero[nf][nc]
        else:
            return self.tablero[of][oc]

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
                    print('..', end = ' ')
                else:
                    if p.get_politica(self.tablero[i][j].id) == 'N':
                        print('NN', end = ' ')
                    if p.get_politica(self.tablero[i][j].id) == 'S':
                        print('SS', end = ' ')
                    if p.get_politica(self.tablero[i][j].id) == 'E':
                        print('EE', end = ' ')
                    if p.get_politica(self.tablero[i][j].id) == 'O':
                        print('OO', end = ' ')
                    if p.get_politica(self.tablero[i][j].id) == 'NE':
                        print('NE', end = ' ')
                    if p.get_politica(self.tablero[i][j].id) == 'NO':
                        print('NO', end = ' ')
                    if p.get_politica(self.tablero[i][j].id) == 'SE':
                        print('SE', end = ' ')
                    if p.get_politica(self.tablero[i][j].id) == 'SO':
                        print('SO', end = ' ')
                    if p.get_politica(self.tablero[i][j].id) is None:
                        print('##', end = ' ')
            print("")
        print("------------------------------------------------------------------------")

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