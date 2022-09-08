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
        algorithm = Value_Iteration(self.hg, self.p, self.V)