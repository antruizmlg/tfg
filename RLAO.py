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

            bpsg_states = self.backward_bpsg_search(self.fs, []) # Obtenemos el best partial solution graph partiendo desde el estado final
            # y expandiendo los antecesores.
            self.hg.update_values(bpsg_states, self.V, self.p) # Actualizamos valores y política de los estados del best partial solution
            # graph

            if all(oldV[s] == self.V[s] for s in oldV.keys()): # Si llegamos a convergencia, salimos del bucle.
                break

    def backward_bpsg_search(self, state, states):
        states.append(state) # Introducimos el estado actual en el conjunto de estados
        predecessors = set(filter(lambda s: not s == state and s not in states, self.hg.get_predecessors(state, self.table)))
        # Obtenemos todos los predecesores del estado actual que no esté ya en el conjunto de estados y que no sea el propio estado
        if predecessors: # Si hay predecesores
            bp = self.hg.best_predecessors(predecessors, self.V)
            states = self.backward_bpsg_search(bp, states) # Llamada recursiva sobre predecesor "greedy"
        return states #Devolvemos lista de estados