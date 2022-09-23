from Graph import *
from copy import *
from Value_Iteration import *

class ILAO:
    def __init__(self, hg, initial_state, h, p, problem):
        self.hg = hg # Hipergrafo
        self.s0 = initial_state.id # Estado inicial
        self.V = h # Función de valor inicializada con el heurístico
        self.p = p # Política inicial
        self.problem = problem

    def ILAO(self):
        bpsg_states = {self.s0}
        expanded = set()
        fringe = {self.s0}
        algorithm = Value_Iteration(self.hg, self.p, self.V)

        while True:
            while bpsg_states & fringe:
                # Expansión hacia adelante
                fringe = self.hg.expand_forward(self.s0, self.V, self.p, expanded, fringe, set())
                # Estados del grafo solución parcial
                bpsg_states = self.hg.get_bpsg_states(self.p, set(), self.s0)

            #Test de convergencia
            algorithm.run(expanded)
            bpsg_states = self.hg.get_bpsg_states(self.p, set(), self.s0)
            if not (bpsg_states & fringe):
                return bpsg_states