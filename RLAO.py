from Graph import *
from Policy_Iteration import *
from Value_Iteration import *
from copy import *

class RLAO:
    def __init__(self, hg, final_state, h, p, table, algorithm):
        self.hg = hg # Hipergrafo
        self.fs = final_state.id # Estado final
        self.V = h # Función de valor inicializada con el heurístico
        self.p = p # Política inicial
        self.table = table
        self.algorithm = algorithm # Nombre del algoritmo a usar. Iteración de política o de valores.

    def RLAO(self):
        F = {self.fs}
        expanded = set()

        # Inicialización grafo explícito y grafo solución
        envelope_graph = Graph({self.fs: []}, self.hg.dict_state)

        # Instanciación objeto algoritmo para su posterior ejecución en cada iteración
        if self.algorithm == 'PI':
            algorithm = Policy_Iteration(self.hg, self.p, self.V) 
        if self.algorithm == 'VI':
            algorithm = Value_Iteration(self.hg, self.p, self.V)

        while F:
            for s in F:
                envelope_graph.states[s] = self.hg.states[s]

            algorithm.run(envelope_graph.states.keys())

            expanded = expanded | F
            F = self.hg.update_fringe_rlao(self.table, F, expanded)