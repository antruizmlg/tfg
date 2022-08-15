from Hipergrafo import *
from PI import *
from VI import *
from copy import *
import time

class RLAO:
    def __init__(self, hg, terminal_state, h, pi, algorithm):
        self.hg = hg # Hipergrafo
        self.sf = terminal_state.id # Estado final
        self.V = h # Función de valor inicializada con el heurístico
        self.p = pi # Política inicial
        self.algorithm = algorithm # Nombre del algoritmo a usar. Iteración de política o de valores.

    def RLAO(self):
        F = [self.sf]
        expanded = [self.sf]

        envelope_graph = Hipergrafo({self.sf: []}, self.hg.dict_state)

        if self.algorithm == 'PI':
            algorithm = PI(self.p, self.V) 
        if self.algorithm == 'VI':
            algorithm = VI(self.p, self.V)

        F = self.hg.predecessor_states(list(set(envelope_graph.estados) & set(F)), expanded)
        while len(F) > 0:
            expanded = list(set(expanded + F))
            self.hg.update_envelope_graph(envelope_graph, F)
            algorithm.run(envelope_graph)
            F = self.hg.predecessor_states(list(set(envelope_graph.estados) & set(F)), expanded)