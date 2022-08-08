from Estado import *
from Hiperarista import *
from Hipergrafo import *
from Politica import *
from FuncionDeValor import *
import random

class Problema:
    def __init__(self, numFilas, numColumnas, numSumideros, probabilidades):

        self.tablero = [[0 for j in range(numColumnas)] for i in range(numFilas)] # Tablero con los estados

        for i in range(numFilas):
            for j in range(numColumnas):
                id = 's' + str(i) + "_" + str(j)
                self.tablero[i][j] = Estado(id) # Rellenamos el tablero con cada estado

        self.ss = Estado('s_ss') 
        self.ss.terminal = True # Añadimos un estado sumidero

        self.filaFinal = self.generador_posicion_final(numFilas - 1) 
        self.columnaFinal = self.generador_posicion_final(numColumnas - 1) # Generamos la fila y columna objetivo. Una de las 4 esquinas aleatoriamente.

        self.tablero[self.filaFinal][self.columnaFinal].terminal = True

        self.filaInicial = numFilas // 2
        self.columnaInicial = numColumnas // 2 # Establecemos el fila y la columna inicial en la mitad del tablero

        self.sumideros = [] # Lista para almacenar la representación en cadena de carácteres de los sumideros

        i = 0
        while i < numSumideros: # Establecemos los sumideros de forma aleatoria. No pueden ser estados terminales ni el estado inical
            numFila = random.randint(0, numFilas - 1)
            numCol = random.randint(0, numColumnas - 1)
            if not self.tablero[numFila][numCol].sumidero and not self.tablero[numFila][numCol].terminal and not (numFila == self.filaInicial and numCol == self.columnaInicial):
                self.tablero[numFila][numCol].sumidero = True
                i += 1
                self.sumideros.append("["+str(numFila)+", "+str(numCol)+"]")

        self.acciones = {'N': 1, 'S': 1, 'E': 1, 'O': 1, '-': 1} # Diccionario con asociación (acción -> coste)
        # La acción "-" representa mantenerse en el mismo estado.

        self.probabilidades = probabilidades # Inicializamos diccionario de probabilidades

    def generar_problema(self):
        dict_state = {} # Diccionario con asociaciones (id de estado -> Objeto estado)
        estados_hg = {} # Diccionario con asociaciones (Estado -> Lista de conectores que salen de ese estado)
        ha_list = [] # Lista para almacenar los k-conectores que salen de un estado concreto
        dict_state[self.ss.id] = self.ss
        for i in range(len(self.tablero)): # Para cada estado en el tablero
            for j in range(len(self.tablero[0])):
                state = self.tablero[i][j] # Obtenemos el estado
                dict_state[state.id] = state # Almacenamos la asociación (id estado -> objeto estado) en el diccionario
                if not state.sumidero: # Si el estado no es sumidero
                    for a in self.acciones.keys(): # Para cada acción posible
                        if not a == '-': # Si la acción implica ir a un estado sucesor (N, S, E, O)
                            ha_list.append(Hiperarista(self.get_probs(i, j, a), a, self.acciones[a]))
                            # Introducimos en la lista de k-conectores para ese estado el k-conector que hace referencia a la acción a.
                else:
                    ha_list.append(Hiperarista({self.ss.id: 1}, 'N', len(self.tablero)*3))
                    # Si es un estado sumidero, ese estado solo tendrá un sucesor con un coste alto, para evitar las transiciones a ese estado.
                estados_hg[state.id] = ha_list
                # Introducimos en el diccionario de estados la asociación (estado id -> lista de k-conectores)
                ha_list = []
                # Vaciamos la lista de k-conectores para el siguiente estado
        hg = Hipergrafo(estados_hg) # Creamos el hipergrafo con el diccionario de estados.
        politica, heuristico = self.get_p_and_h() # Obtenemos la política inicial y el heurístico
        return dict_state, hg, self.tablero[self.filaInicial][self.columnaInicial], heuristico, politica 
        # Devolvemos el diccionario con asociaciones (id de estado -> objeto estado), el hipergrafo que representa el problema, el estado inicial,
        # el heurístico y la política inicial

    """método que recibe una fila, una columna y una acción, y devuelve un diccionario con asociaciones (estado -> probabilidad) asociada al
    k-conector que sale del estado en la posición (fila, columna) del tablero al realizar la acción 'a' """
    def get_probs(self, fila, columna, accion):
        probs = {}

        for a in self.probabilidades[accion].keys():
            suc = self.successor(fila, columna, a)
            if suc.id in probs.keys():
                probs[suc.id] += self.probabilidades[accion][a]
            else:
                probs[suc.id] = self.probabilidades[accion][a]
        return probs

    """método que recibe una fila, una columna y una acción y devuelve el sucesor directo de realizar esa acción desde esa fila y esa columna del tablero"""
    def successor(self, fila, columna, accion):
        if accion == 'N':
            return self.get_successor_state(fila, columna, fila - 1, columna)
        if accion == 'S':
            return self.get_successor_state(fila, columna, fila + 1, columna)
        if accion == 'E':
            return self.get_successor_state(fila, columna, fila, columna + 1)            
        if accion == 'O':
            return self.get_successor_state(fila, columna, fila, columna - 1)
        if accion == '-':
            return self.tablero[fila][columna]

    def get_successor_state(self, of, oc, nf, nc):
        if nf >= 0 and nf < len(self.tablero) and nc >= 0 and nc < len(self.tablero[0]): # Si la acción lleva a una posición valida del tablero
            return self.tablero[nf][nc] # Devolvemos el sucesor
        else: # De lo contrario
            return self.tablero[of][oc] # Hemos salido del tablero, devolvemos el mismo estado

    """Método para imprimir información del problema"""
    def print_info(self):   
        print("Tamaño de tablero: " + str(len(self.tablero)) + "x" + str(len(self.tablero[0])))
        for s in self.sumideros:
                print("Sumidero: "+ s)
        print("Celda inicial: [" + str(self.filaInicial) + ", " + str(self.columnaInicial) + "]")
        print("Celda objetivo: [" + str(self.filaFinal) + ", " + str(self.columnaFinal) + "]\n")

    """Método para imprimir el tablero con la solución dada la política óptima"""
    def print_solution(self, p):
        print("------------------------------------------------------------------------")
        for i in range(len(self.tablero)):
            for j in range(len(self.tablero[0])):
                state = self.tablero[i][j]
                if state.terminal:
                    print('TT', end = ' ')
                elif state.sumidero:
                    print('..', end = ' ')
                else:
                    if p.get_politica(state.id) == 'N':
                        print('NN', end = ' ')
                    if p.get_politica(state.id) == 'S':
                        print('SS', end = ' ')
                    if p.get_politica(state.id) == 'E':
                        print('EE', end = ' ')
                    if p.get_politica(state.id) == 'O':
                        print('OO', end = ' ')
                    if p.get_politica(state.id) is None:
                        print('##', end = ' ')
            print("")
        print("------------------------------------------------------------------------")

    """Método para obtener política inicial y heurístico"""
    def get_p_and_h(self):
        politica = {}
        heuristico = {}
        for i in range(len(self.tablero)): 
            for j in range(len(self.tablero[i])):
                state = self.tablero[i][j]
                politica[state.id] = None 
                heuristico[state.id] = state.h_MD(i, j, self.filaFinal, self.columnaFinal) 
        politica[self.ss.id] = None
        heuristico[self.ss.id] = 0
        return Politica(politica), FuncionDeValor(heuristico)

    @staticmethod
    def generador_posicion_final(p):
        if random.randint(0, 1) == 0:
            return 0
        else:
            return p