from Graph import *
from Policy_Iteration import *
from Value_Iteration import *
from copy import *
import time

class RLAO:
    def __init__(self, hg, final_state, h, p, algorithm):
        self.hg = hg # Hipergrafo
        self.fs = final_state.id # Estado final
        self.V = h # Función de valor inicializada con el heurístico
        self.p = p # Política inicial
        self.algorithm = algorithm # Nombre del algoritmo a usar. Iteración de política o de valores.