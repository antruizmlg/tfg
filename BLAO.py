from Graph import *
from Policy_Iteration import *
from Value_Iteration import *
from copy import *

class BLAO:
    def __init__(self, hg, initial_state, final_state, h, p, table, algorithm):
        self.hg = hg # Hipergrafo
        self.s0 = initial_state.id
        self.fs = final_state.id # Estado final
        self.V = h # Función de valor inicializada con el heurístico
        self.p = p # Política inicial
        self.table = table
        self.algorithm = algorithm # Nombre del algoritmo a usar. Iteración de política o de valores.

    def BLAO(self):
        F = {self.s0}
        I = set()

        F_backward = {self.fs}

        envelope_graph = Graph({self.s0: []}, self.hg.dict_state)
        backward_envelope_graph = Graph({self.fs: self.hg.states[self.fs]}, self.hg.dict_state)

        while True:
            oldV = deepcopy(self.V)

            stack_DFS = [] 
            F = self.hg.depth_first_search(envelope_graph, self.s0, F, I, self.p, stack_DFS)

            stack_Backward = []
            F_backward = self.hg.backward_search(self, backward_envelope_graph, self.fs, F_backward, I, self.V, self.s0, stack_Backward)

            self.hg.update_values(stack_DFS, self.V, self.p)
            self.hg.update_values(stack_Backward, self.V, self.p)

            if all(oldV[s] == self.V[s] for s in oldV.keys()): # Si llegamos a convergencia, salimos del bucle.
                break