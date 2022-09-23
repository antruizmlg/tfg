from Graph import *
from Value_Iteration import *
from copy import *

class BLAO:
    def __init__(self, hg, initial_state, final_state, h, p, problem):
        self.hg = hg # Hipergrafo
        self.s0 = initial_state.id
        self.fs = final_state.id # Estado final
        self.V = h # Función de valor inicializada con el heurístico
        self.p = p # Política inicial
        self.problem = problem

    def BLAO(self):
        bpsg_states = {self.s0}
        expanded = set()
        fringe = {self.s0, self.fs}
        algorithm = Value_Iteration(self.hg, self.p, self.V)

        while True:
            while bpsg_states & fringe:
                updated = set()
                # Expansión hacia adelante
                fringe = self.hg.expand_forward(self.s0, self.V, self.p, expanded, fringe, updated)
                # Expansión hacia atrás
                fringe = self.hg.expand_backward(self.fs, self.V, self.p, self.problem.table, expanded, fringe, self.s0, updated)
                # Estados del grafo solución parcial
                bpsg_states = self.hg.get_bpsg_states(self.p, set(), self.s0)
                
            #Test de convergencia
            algorithm.run(expanded)
            bpsg_states = self.hg.get_bpsg_states(self.p, set(), self.s0)
            if not (bpsg_states & fringe):
                return bpsg_states