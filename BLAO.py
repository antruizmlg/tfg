from Graph import *
from Policy_Iteration import *
from Value_Iteration import *
from copy import *

class BLAO:
    def __init__(self, hg, initial_state, final_state, h, p, table, algorithm):
        self.hg = hg # Hipergrafo
        self.s0 = initial_state.id
        self.fs = final_state.id # Estado final
        self.V = h # Función de valor inicializada con el heurístico
        self.p = p # Política inicial
        self.table = table
        self.algorithm = algorithm # Nombre del algoritmo a usar. Iteración de política o de valores.

    def BLAO(self):
        # Conjuntos de estados "fringe" e "interior"
        F = {self.s0}
        I = set()

        Q = {s: {'N': 1, 'S': 1, 'E': 1, 'O': 1} for k in self.hg.states.keys()}
        Q[self.fs] = {'N': 0, 'S': 0, 'E': 0, 'O': 0}

        dict_suc = {}
        for s in self.hg.states.keys():
            dict_suc[s] = self.get_successors(s)

        forward_graph = Graph({self.s0: []}, self.hg.dict_state)
        reverse_graph = Graph({self.fs: []}, self.hg.dict_state)

        bpsg_states = {self.s0}

        # Instanciación objeto algoritmo para su posterior ejecución en cada iteración
        if self.algorithm == 'PI':
            algorithm = Policy_Iteration(self.hg, self.p, self.V) 
        if self.algorithm == 'VI':
            algorithm = Value_Iteration(self.hg, self.p, self.V)

        s = self.hg.get_no_final_state(bpsg_states & F) # Obtenemos un estado no terminal del conjunto de estados "fringe" del grafo solución

        while s is not None: # Mientras queden estados por expandir
            self.hg.update_fringe_set(F, I, s) # Actualizamos el conjunto F
            F.remove(s) # Eliminamos el estado s del conjunto fringe
            I.add(s) # Introducimos s en el conjunto I
            forward_graph.states[s] = self.hg.states[s] # Actualizamos grafo explícito

    def get_successors(self, state):
        actions = ['N', 'S', 'E', 'O']
        dict = {}
        for a in actions:
            c = self.hg.get_connector(state, a)
            dict[a] = max(c.probs, key=c.probs.get)
        return dict