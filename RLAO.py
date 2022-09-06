from configparser import InterpolationError
from Graph import *
from Value_Iteration import *
from copy import *

class RLAO:
    def __init__(self, hg, s0,final_state, h, p, problem):
        self.hg = hg # Hipergrafo
        self.s0 = s0.id
        self.fs = final_state.id # Estado final
        self.V = h # Función de valor inicializada con el heurístico
        self.p = p # Política inicial
        self.table = problem.table
        self.problem = problem

    def RLAO(self):
        I = set() # Conjunto interior. Este conjunto es compartido, los nodos se expanden buscando hacia atrás o hacia adelante.
        F = {self.fs} # Conjunto fringe búsqueda hacia atrás

        algorithm = Value_Iteration(self.hg, self.p, self.V)
        # Inicialización grafo explícito
        envelope_graph = Graph({self.fs: self.hg.states[self.fs]}, self.hg.dict_state)
        stack = []

        while True:
            oldV = deepcopy(self.V)

            F = self.hg.backward_search(envelope_graph, self.fs, F, I, self.V, '', self.table, [], stack)
            self.hg.update_values(stack, self.V, self.p) 

            #Test de convergencia
            bpsg_states = self.hg.get_bpsg_states(envelope_graph, self.p, set(), self.s0)
            algorithm.run(bpsg_states)
            #Test de convergencia
            if all(oldV[s] == self.V[s] for s in oldV.keys()) and bpsg_states: 
                break