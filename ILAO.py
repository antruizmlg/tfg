from inspect import stack
from tkinter import S
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
        algorithm = Value_Iteration(self.hg, self.p, self.V)

        while True:
            old_policy = deepcopy(self.p)

            while (bpsg_states - expanded):
                self.hg.expand_forward(self.s0, self.V, self.p, expanded, set())
                bpsg_states = self.hg.get_bpsg_states(self.p, set(), self.s0)
            #Test de convergencia
            algorithm.run(bpsg_states)
            bpsg_states = self.hg.get_bpsg_states(self.p, set(), self.s0)

            if all(old_policy[s] == self.p[s] for s in old_policy.keys()):
                break