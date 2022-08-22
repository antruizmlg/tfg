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
        while True:
            oldV = deepcopy(self.V) 

            bpsg_states = self.get_bpsg_states(self.fs, []) # Obtenemos el best partial solution graph partiendo desde el estado final
            # y expandiendo los antecesores.
            self.hg.update_values(bpsg_states, self.V, self.p) # Actualizamos valores y política de los estados del best partial solution
            # graph

            if all(oldV[s] == self.V[s] for s in oldV.keys()): # Si llegamos a convergencia, salimos del bucle.
                break

    def get_bpsg_states(self, state, states):
        states.append(state)
        predecessors = set(filter(lambda s: not s == state and s not in states, self.hg.get_predecessors(state, self.table)))
        if predecessors:
            min_value = float('inf')
            for pred in predecessors:
                if self.V[pred] < min_value:
                    min_value = self.V[pred]
                    best_pred = pred
            states = self.get_bpsg_states(best_pred, states)
        return states