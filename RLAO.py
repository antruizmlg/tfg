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
        self.problem = problem

    def RLAO(self):
        F = {self.fs}
        I = set()
        envelope_graph = Graph({self.fs: []}, self.hg.dict_state)
        algorithm = Value_Iteration(self.hg, self.p, self.V)

        while True: 
            old_p = deepcopy(self.p)

            self.expand(self.fs, set())

            #Test de convergencia
            bpsg_states = self.hg.get_bpsg_states(envelope_graph, self.p, set(), self.s0)
            if bpsg_states:
                algorithm.run(bpsg_states) # Aplicamos VI sobre los estados del grafo solución parcial
                if all(old_p[s] == self.p[s] for s in old_p.keys()): # Si llegamos a convergencia, salimos del bucle
                    break

    def expand(self, s, expanded):
        expanded.add(s)
        self.hg.update_values([s], self.V, self.p)
        predecessors = set(filter(lambda s: s not in expanded, self.hg.get_predecessors(s, self.problem.table)))
        if predecessors:
            bp = self.hg.best_predecessor(predecessors, self.V)
            self.expand(bp, expanded)