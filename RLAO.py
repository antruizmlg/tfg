from configparser import InterpolationError
from Graph import *
from Value_Iteration import *
from copy import *

class RLAO:
    def __init__(self, hg, final_state, h, p, table):
        self.hg = hg # Hipergrafo
        self.fs = final_state.id # Estado final
        self.V = h # Función de valor inicializada con el heurístico
        self.p = p # Política inicial
        self.table = table

    def RLAO(self):
        bpsg_states = []

        while True:
            old_bpsg = deepcopy(bpsg_states) 

            bpsg_states = self.get_bpsg_states(self.fs, []) # Obtenemos el best partial solution graph partiendo desde el estado final
            # y expandiendo los antecesores.
            self.hg.update_values(bpsg_states, self.V, self.p) # Actualizamos valores y política de los estados del best partial solution
            # graph

            if set(bpsg_states) == set(old_bpsg): # Si llegamos a convergencia, salimos del bucle.
                break

    def get_bpsg_states(self, state, states):
        states.append(state) # Introducimos el estado actual en el conjunto de estados
        predecessors = set(filter(lambda s: not s == state and s not in states, self.hg.get_predecessors(state, self.table)))
        # Obtenemos todos los predecesores del estado actual que no esté ya en el conjunto de estados y que no sea el propio estado
        if predecessors: # Si hay predecesores
            min_value = float('inf')
            for pred in predecessors:
                if self.V[pred] < min_value:
                    min_value = self.V[pred]
                    best_pred = pred # Obtenemos el mejor predecesor "greedy"
            states = self.get_bpsg_states(best_pred, states) # Llamada recursiva sobre predecesor "greedy"
        return states #Devolvemos lista de estados