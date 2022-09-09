from State import *
from Connector import *
from Graph import *
import random

class Problem:
    def __init__(self, x, y, w, z, sinks, probs):
        self.table = [[[[0 for _ in range(z)] for _ in range(w)] for _ in range(y)] for _ in range(x)]
        for i in range(x):
            for j in range(y):
                for k in range(w):
                    for l in range(z):
                        self.table[i][j][k][l] = State('s' + str(i) + '_'  + str(j) + '_'  + str(k) + '_'  + str(l), i, j, k, l)

        """ el estado final será una esquina aleatoria del tablero """
        self.x_final = self.first_or_last_random(x)
        self.y_final = self.first_or_last_random(y)
        self.w_final = self.first_or_last_random(w)
        self.z_final = self.first_or_last_random(z)
        self.table[self.x_final][self.y_final][self.w_final][self.z_final].final = True

        self.initial_x = x // 2
        self.initial_y = y // 2
        self.initial_w = w // 2
        self.initial_z = z // 2

        while sinks: # Establecemos los sumideros de forma aleatoria. No pueden ser estados terminales ni el estado inical.
            x_ = random.randint(0, x - 1)
            y_ = random.randint(0, y - 1)
            w_ = random.randint(0, w - 1)
            z_ = random.randint(0, z - 1)
            if not self.table[x_][y_][w_][z_].sink and not x_ == self.initial_x and not x_ == self.x_final:
                self.table[x_][y_][w_][z_].sink = True
                sinks -= 1

        self.actions = {}
        for action in probs.keys():
            self.actions[action] = 1
        self.actions['-'] = 1
        self.probs = probs # Inicializamos diccionario de probabilidades

    def generate_problem(self):
        dict_state = {} # Diccionario con asociaciones (id de estado -> Objeto estado)
        states_hg = {} # Diccionario con asociaciones (Estado -> Lista de conectores que salen de ese estado)

        for i in range(len(self.table)): # Para cada estado en el tablero
            for j in range(len(self.table[0])):
                for k in range(len(self.table[0][0])):
                    for l in range(len(self.table[0][0][0])):                
                        state = self.table[i][j][k][l] # Obtenemos el estado
                        dict_state[state.id] = state # Almacenamos la asociación (id estado -> objeto estado) en el diccionario
                        c_list = [] # Lista para almacenar los k-conectores que salen de un estado concreto
                        if not state.final: # Si el estado no es terminal
                            if not state.sink: # Si el estado no es sumidero
                                for a in set(filter(lambda action: not action == '-', self.actions.keys())): # Para cada acción posible que implica ir a un estado sucesor
                                    probs_trans = self.get_probs(i, j, k, l, a)
                                    if probs_trans:
                                        c_list.append(Connector(probs_trans, a, self.actions[a]))
                                    # Introducimos en la lista de k-conectores para ese estado el k-conector que hace referencia a la acción a.
                        states_hg[state.id] = c_list # Introducimos en el diccionario de estados la asociación (estado id -> lista de k-conectores)
        hg = Graph(states_hg, dict_state) # Creamos el hipergrafo con el diccionario de estados.
        return hg, self.table[self.initial_x][self.initial_y][self.initial_w][self.initial_z], self.table[self.x_final][self.y_final][self.w_final][self.z_final]
        # Devolvemos el hipergrafo que representa el problema, el estado inicial y el estado final

    """método que recibe una fila, una columna y una acción, y devuelve un diccionario con asociaciones (estado -> probabilidad) asociada al
    k-conector que sale del estado en la posición (fila, columna) del tablero al realizar la acción 'a' """
    def get_probs(self, x, y, w, z, action):
        probs = {}

        for a in self.probs[action].keys():
            suc = self.successor(x, y, w, z, a)
            if suc.sink:
                return {}
            if suc.id in probs.keys():
                probs[suc.id] += self.probs[action][a]
            else:
                probs[suc.id] = self.probs[action][a]
        return probs

    """método que recibe una fila, una columna y una acción y devuelve el sucesor directo de realizar esa acción desde esa fila y esa columna del tablero"""
    def successor(self, x, y, w, z, action):
        if action == '1':
            return self.get_successor_state(x, y, w, z, x + 1, y, w, z)
        if action == '2':
            return self.get_successor_state(x, y, w, z, x - 1, y, w, z)
        if action == '3':
            return self.get_successor_state(x, y, w, z, x, y + 1, w, z)            
        if action == '4':
            return self.get_successor_state(x, y, w, z, x, y - 1, w, z)
        if action == '5':
            return self.get_successor_state(x, y, w, z, x, y, w + 1, z)
        if action == '6':
            return self.get_successor_state(x, y, w, z, x, y, w - 1, z)
        if action == '7':
            return self.get_successor_state(x, y, w, z, x, y, w, z + 1)            
        if action == '8':
            return self.get_successor_state(x, y, w, z, x, y, w, z - 1)
        if action == '-':
            return self.table[x][y][w][z]

    def get_successor_state(self, x, y, w, z, x_, y_, w_, z_):
        if self.valid_dimension(x_, len(self.table)) and self.valid_dimension(y_, len(self.table[0])) and self.valid_dimension(w_, len(self.table[0][0])) and self.valid_dimension(z_, len(self.table[0][0][0])): # Si la acción lleva a una posición valida del tablero
            return self.table[x_][y_][w_][z_] # Devolvemos el sucesor
        else: # De lo contrario
            return self.table[x][y][w][z] # Hemos salido del tablero, devolvemos el mismo estado

    """Método para imprimir información del problema"""
    def print_info(self):
        print("---------------PROBLEMA GENERADO---------------")   
        print("Tamaño de tablero: " + str(len(self.table)) + "x" + str(len(self.table[0])) + "x" + str(len(self.table[0][0])) + "x" + str(len(self.table[0][0][0])))
        print("Número total de estados: "+str(len((self.table)*len(self.table[0])*len(self.table[0][0])*len(self.table[0][0][0]))))
        print("Celda inicial: [" + str(self.initial_x) + ", " + str(self.initial_y) + ", " + str(self.initial_w) + ", " + str(self.initial_z) + "]")
        print("Celda objetivo: [" + str(self.x_final) + ", " + str(self.y_final) + ", " + str(self.w_final) + ", " + str(self.z_final) + "]")
        print("-----------------------------------------------")   

    """Método para obtener política inicial y heurístico"""
    def get_initial_policy_and_heuristic(self, algorithm):
        p = {}
        h = {}
        for i in range(len(self.table)): 
            for j in range(len(self.table[0])):
                for k in range(len(self.table[0][0])):
                    for l in range(len(self.table[0][0][0])):
                        state = self.table[i][j][k][l]
                        p[state.id] = None
                        if algorithm == 'VI':
                            h[state.id] = 0
                        else:
                            h[state.id] = state.h_MD(i, self.x_final, j, self.y_final, k, self.w_final, l, self.z_final)
        return p, h

    @staticmethod
    def first_or_last_random(number):
        if random.randint(0, 1) == 0:
            return 0
        else:
            return number - 1

    @staticmethod
    def valid_dimension(number, total_dim):
        return number >= 0 and number < total_dim