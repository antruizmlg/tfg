from State import *
from Connector import *
from Graph import *
import random

class Problem:
    def __init__(self, rows, columns, sinks, probs):

        self.table = [[0 for j in range(rows)] for i in range(columns)] # Tablero con los estados

        for i in range(rows):
            for j in range(columns):
                id = 's' + str(i) + "_" + str(j)
                self.table[i][j] = State(id, i, j) # Rellenamos el tablero con cada estado

        self.ss = State('s_ss', '', '') 
        self.ss.final = True # Añadimos un estado sumidero

        self.final_row = self.random_generator(rows - 1) 
        self.final_col = self.random_generator(columns - 1) # Generamos la fila y columna objetivo. Una de las 4 esquinas aleatoriamente.

        self.table[self.final_row][self.final_col].final = True

        self.initial_row = rows // 2
        self.initial_col = columns // 2 # Establecemos el fila y la columna inicial en la mitad del tablero

        self.sinks = [] # Lista para almacenar la representación en cadena de carácteres de los sumideros

        i = 0
        while i < sinks: # Establecemos los sumideros de forma aleatoria. No pueden ser estados terminales ni el estado inical
            r = random.randint(0, rows - 1)
            c = random.randint(0, columns - 1)
            if not self.table[r][c].sink and not self.table[r][c].final and not (r == self.initial_row and c == self.initial_row):
                self.table[r][c].sink = True
                self.sinks.append("["+str(r)+", "+str(c)+"]")
                i += 1

        self.actions = {'N': 1, 'S': 1, 'E': 1, 'O': 1, '-': 1} # Diccionario con asociación (acción -> coste)
        # La acción "-" representa mantenerse en el mismo estado.

        self.probs = probs # Inicializamos diccionario de probabilidades

    def generate_problem(self):
        dict_state = {} # Diccionario con asociaciones (id de estado -> Objeto estado)
        states_hg = {} # Diccionario con asociaciones (Estado -> Lista de conectores que salen de ese estado)
        c_list = [] # Lista para almacenar los k-conectores que salen de un estado concreto
        dict_state[self.ss.id] = self.ss

        for i in range(len(self.table)): # Para cada estado en el tablero
            for j in range(len(self.table[0])):
                state = self.table[i][j] # Obtenemos el estado
                dict_state[state.id] = state # Almacenamos la asociación (id estado -> objeto estado) en el diccionario
                if not state.sink: # Si el estado no es sumidero
                    for a in self.actions.keys(): # Para cada acción posible
                        if not a == '-': # Si la acción implica ir a un estado sucesor (N, S, E, O)
                            c_list.append(Connector(self.get_probs(i, j, a), a, self.actions[a]))
                            # Introducimos en la lista de k-conectores para ese estado el k-conector que hace referencia a la acción a.
                else:
                    c_list.append(Connector({self.ss.id: 1}, 'N', len(self.table)*3))
                    # Si es un estado sumidero, ese estado solo tendrá un sucesor con un coste alto, para evitar las transiciones a ese estado.
                states_hg[state.id] = c_list
                # Introducimos en el diccionario de estados la asociación (estado id -> lista de k-conectores)
                c_list = []
                # Vaciamos la lista de k-conectores para el siguiente estado
        hg = Graph(states_hg, dict_state) # Creamos el hipergrafo con el diccionario de estados.
        return hg, self.table[self.initial_row][self.initial_col], self.table[self.final_row][self.final_col]
        # Devolvemos el diccionario con asociaciones (id de estado -> objeto estado), el hipergrafo que representa el problema, el estado inicial

    """método que recibe una fila, una columna y una acción, y devuelve un diccionario con asociaciones (estado -> probabilidad) asociada al
    k-conector que sale del estado en la posición (fila, columna) del tablero al realizar la acción 'a' """
    def get_probs(self, row, col, action):
        probs = {}

        for a in self.probs[action].keys():
            suc = self.successor(row, col, a)
            if suc.id in probs.keys():
                probs[suc.id] += self.probs[action][a]
            else:
                probs[suc.id] = self.probs[action][a]
        return probs

    """método que recibe una fila, una columna y una acción y devuelve el sucesor directo de realizar esa acción desde esa fila y esa columna del tablero"""
    def successor(self, row, col, action):
        if action == 'N':
            return self.get_successor_state(row, col, row - 1, col)
        if action == 'S':
            return self.get_successor_state(row, col, row + 1, col)
        if action == 'E':
            return self.get_successor_state(row, col, row, col + 1)            
        if action == 'O':
            return self.get_successor_state(row, col, row, col - 1)
        if action == '-':
            return self.table[row][col]

    def get_successor_state(self, of, oc, nf, nc):
        if nf >= 0 and nf < len(self.table) and nc >= 0 and nc < len(self.table[0]): # Si la acción lleva a una posición valida del tablero
            return self.table[nf][nc] # Devolvemos el sucesor
        else: # De lo contrario
            return self.table[of][oc] # Hemos salido del tablero, devolvemos el mismo estado

    """Método para imprimir información del problema"""
    def print_info(self):   
        print("Tamaño de tablero: " + str(len(self.table)) + "x" + str(len(self.table[0])))
        for s in self.sinks:
            print("Sumidero: "+ s)
        print("Celda inicial: [" + str(self.initial_row) + ", " + str(self.initial_col) + "]")
        print("Celda objetivo: [" + str(self.final_row) + ", " + str(self.final_col) + "]\n")

    """Métodos para imprimir el tablero con la solución dada la política óptima"""

    def print_solution(self, p):
        dic = {}
        self.get_solution(p, self.initial_row, self.initial_col, dic)
        for i in range(len(self.table)):
            for j in range(len(self.table[0])):
                if self.table[i][j].final:
                    print('T', end=" ")
                elif self.table[i][j].sink:
                    print('.', end=" ")
                elif self.table[i][j] in dic.keys():
                    print(dic[self.table[i][j]], end=" ")
                else:
                    print('#', end=" ")
            print("")

    def get_solution(self, p, fil, col, dic):
        state = self.table[fil][col]
        if not state.final:
            action = p[state.id]
            dic[state] = action
            if action == 'N':
                self.get_solution(p, fil - 1, col, dic)
            if action == 'S':
                self.get_solution(p, fil + 1, col, dic)
            if action == 'E':
                self.get_solution(p, fil, col + 1, dic)
            if action == 'O':
                self.get_solution(p, fil, col - 1, dic)

    """Método para obtener política inicial y heurístico"""
    def get_initial_policy_and_heuristic(self, heuristic):
        policy = {}
        heuristic = {}
        for i in range(len(self.table)): 
            for j in range(len(self.table[i])):
                state = self.table[i][j]
                policy[state.id] = None
                if heuristic == 'MD': 
                    heuristic[state.id] = state.h_MD(i, j, self.final_row, self.final_col)
                else:
                    heuristic[state.id] = 0
        policy[self.ss.id] = None
        heuristic[self.ss.id] = 0
        return policy, heuristic

    @staticmethod
    def random_generator(p):
        if random.randint(0, 1) == 0:
            return 0
        else:
            return p