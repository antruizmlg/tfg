from configparser import InterpolationError
from re import I
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
        bpsg_states = {self.s0}
        expanded = set()
        fringe = {self.fs, self.s0}
        algorithm = Value_Iteration(self.hg, self.p, self.V)

        it = 0

        while True:
            while (bpsg_states & fringe):
                fringe = self.hg.expand_backward(self.fs, self.V, self.p, self.problem.table, expanded, fringe, self.s0, set())
                bpsg_states = self.hg.get_bpsg_states(self.p, set(), self.s0)
                it += 1

            #Test de convergencia
            algorithm.run(expanded)
            bpsg_states = self.hg.get_bpsg_states(self.p, set(), self.s0)
            if not (bpsg_states & fringe):
                return len(expanded), it