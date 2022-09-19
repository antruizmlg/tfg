from State import *
from Connector import *
from Graph import *
import random

class Problem:
    def __init__(self, rows, columns, sinks, probs):
        self.table = [] # Tablero con los estados

        for i in range(rows):
            row = []
            for j in range(columns):
                row.append(State('s' + str(i) + "_" + str(j), i, j)) # Rellenamos el tablero con cada estado
            self.table.append(row)

        """ el estado final será una esquina aleatoria del tablero """
        self.final_row = random.randrange(0, rows - 1, rows - 1) 
        self.final_col = random.randrange(0, columns - 1, columns - 1) 
        self.table[self.final_row][self.final_col].final = True

        self.initial_row = rows // 2
        self.initial_col = columns // 2 # Establecemos el fila y la columna inicial en la mitad del tablero

        while sinks: # Establecemos los sumideros de forma aleatoria. No pueden ser estados terminales ni el estado inical.
            r = random.randint(0, rows - 1)
            c = random.randint(0, columns - 1)
            if not self.table[r][c].sink and not r == self.initial_row and not c == self.final_col:
                self.table[r][c].sink = True
                sinks -= 1

        self.probs = probs # Inicializamos diccionario de probabilidades

    def generate_problem(self):
        dict_state = {} # Diccionario con asociaciones (id de estado -> Objeto estado)
        states_hg = {} # Diccionario con asociaciones (Estado -> Lista de conectores que salen de ese estado)

        for i in range(len(self.table)): # Para cada estado en el tablero
            for j in range(len(self.table[0])):
                state = self.table[i][j] # Obtenemos el estado
                dict_state[state.id] = state # Almacenamos la asociación (id estado -> objeto estado) en el diccionario
                c_list = [] # Lista para almacenar los k-conectores que salen de un estado concreto
                if not state.final and not state.sink: # Si el estado no es terminal ni sumidero
                    for a in {'NN', 'SS', 'EE', 'OO', 'NE', 'NO', 'SE', 'SO', '--'}: # Para cada acción posible que implica ir a un estado sucesor
                        probs_trans = self.get_probs(i, j, a)
                        if probs_trans:
                            c_list.append(Connector(probs_trans, a, 1))
                            # Introducimos en la lista de k-conectores para ese estado el k-conector que hace referencia a la acción a.
                states_hg[state.id] = c_list # Introducimos en el diccionario de estados la asociación (estado id -> lista de k-conectores)
        hg = Graph(states_hg, dict_state) # Creamos el hipergrafo con el diccionario de estados.
        return hg, self.table[self.initial_row][self.initial_col], self.table[self.final_row][self.final_col]
        # Devolvemos el hipergrafo que representa el problema, el estado inicial y el estado final

    """método que recibe una fila, una columna y una acción, y devuelve un diccionario con asociaciones (estado -> probabilidad) asociada al
    k-conector que sale del estado en la posición (fila, columna) del tablero al realizar la acción 'a' """
    def get_probs(self, row, col, action):
        probs = {}

        for a in self.probs[action].keys():
            suc = self.successor(row, col, a)
            if suc.sink:
                return {}
            if suc.id in probs.keys():
                probs[suc.id] += self.probs[action][a]
            else:
                probs[suc.id] = self.probs[action][a]
        return probs

    """método que recibe una fila, una columna y una acción y devuelve el sucesor directo de realizar esa acción desde esa fila y esa columna del tablero"""
    def successor(self, row, col, action):
        if action == 'NN':
            return self.get_successor_state(row, col, row - 1, col)
        if action == 'SS':
            return self.get_successor_state(row, col, row + 1, col)
        if action == 'EE':
            return self.get_successor_state(row, col, row, col + 1)            
        if action == 'OO':
            return self.get_successor_state(row, col, row, col - 1)
        if action == 'NE':
            return self.get_successor_state(row, col, row - 1, col + 1)
        if action == 'SE':
            return self.get_successor_state(row, col, row + 1, col + 1)
        if action == 'NO':
            return self.get_successor_state(row, col, row - 1, col - 1)            
        if action == 'SO':
            return self.get_successor_state(row, col, row + 1, col - 1)
        if action == '--':
            return self.table[row][col]

    def get_successor_state(self, of, oc, nf, nc):
        if nf >= 0 and nf < len(self.table) and nc >= 0 and nc < len(self.table[0]): # Si la acción lleva a una posición valida del tablero
            return self.table[nf][nc] # Devolvemos el sucesor
        else: # De lo contrario
            return self.table[of][oc] # Hemos salido del tablero, devolvemos el mismo estado

    """Método para imprimir información del problema"""
    def print_info(self):
        print("---------------PROBLEMA GENERADO---------------")   
        print("Tamaño de tablero: " + str(len(self.table)) + "x" + str(len(self.table[0])))
        print("Celda inicial: [" + str(self.initial_row) + ", " + str(self.initial_col) + "]")
        print("Celda objetivo: [" + str(self.final_row) + ", " + str(self.final_col) + "]")
        print("-----------------------------------------------")   

    """Métodos para imprimir el tablero con la solución dada la política óptima"""

    def print_solution(self, p):
        dic = {}
        str = ""
        self.get_solution(p, self.initial_row, self.initial_col, dic)
        for i in range(len(self.table)):
            for j in range(len(self.table[0])):
                if self.table[i][j].final:
                    str += 'TT '
                elif self.table[i][j].sink:
                    str += '## '
                elif self.table[i][j] in dic.keys():
                    str += dic[self.table[i][j]] + ' '
                else:
                    str += '.. '
            str += '\n'
        return str

    def get_solution(self, p, fil, col, dic):
        state = self.table[fil][col]
        if not state.final:
            action = p[state.id]
            dic[state] = action
            if action == 'NN':
                self.get_solution(p, fil - 1, col, dic)
            if action == 'SS':
                self.get_solution(p, fil + 1, col, dic)
            if action == 'EE':
                self.get_solution(p, fil, col + 1, dic)
            if action == 'OO':
                self.get_solution(p, fil, col - 1, dic)
            if action == 'NE':
                self.get_solution(p, fil - 1, col + 1, dic)
            if action == 'SE':
                self.get_solution(p, fil + 1, col + 1, dic)
            if action == 'NO':
                self.get_solution(p, fil - 1, col - 1, dic)
            if action == 'SO':
                self.get_solution(p, fil + 1, col - 1, dic)

    def print_table(self, p):
        for i in range(len(self.table)):
            for j in range(len(self.table[0])):
                state = self.table[i][j]            
                if state.final:
                    print('TT', end=" ")
                elif state.sink:
                    print('##', end=" ")
                else:
                    action = p[state.id]
                    if action is None:
                        print('..', end=" ")
                    else:
                        print(action, end=" ")                
            print("")

    """Método para obtener política inicial y heurístico"""
    def get_initial_policy_and_heuristic(self, algorithm):
        p = {}
        h = {}
        for i in range(len(self.table)): 
            for j in range(len(self.table[i])):
                state = self.table[i][j]
                p[state.id] = None
                if algorithm == 'VI':
                    h[state.id] = 0
                else:
                    h[state.id] = state.h(i, self.final_row, j, self.final_col)
        return p, h