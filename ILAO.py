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
        algorithm = Value_Iteration(self.hg, self.p, self.V)
        while True:
            old_p = deepcopy(self.p)

            self.hg.expand_forward(self.s0, self.V, self.p, set())
            #Test de convergencia
            bpsg_states = self.hg.get_bpsg_states(self.p, set(), self.s0)
            algorithm.run(bpsg_states) # Aplicamos VI sobre los estados del grafo solución parcial
            if all(old_p[s] == self.p[s] for s in old_p.keys()): # Si llegamos a convergencia, salimos del bucle
                break