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
        algorithm = Value_Iteration(self.hg, self.p, self.V)

        while True: 
            old_p = deepcopy(self.p)

            self.hg.expand_backward(self.fs, self.V, self.p, self.problem.table, set())
            #Test de convergencia
            bpsg_states = self.hg.get_bpsg_states(self.p, set(), self.s0)
            if len(bpsg_states) > 1:
                algorithm.run(bpsg_states) # Aplicamos VI sobre los estados del grafo solución parcial
                if all(old_p[s] == self.p[s] for s in old_p.keys()): # Si llegamos a convergencia, salimos del bucle
                    break