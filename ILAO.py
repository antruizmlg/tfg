from inspect import stack
from Graph import *
from Policy_Iteration import *
from Value_Iteration import *
from copy import *
import time

class ILAO:
    def __init__(self, hg, initial_state, h, p, table, algorithm):
        self.hg = hg # Hipergrafo
        self.s0 = initial_state.id # Estado inicial
        self.V = h # Función de valor inicializada con el heurístico
        self.p = p # Política inicial
        self.table = table
        self.algorithm = algorithm # Nombre del algoritmo a usar. Iteración de política o de valores.

    def ILAO(self):
        # Conjuntos de estados "fringe" e "interior"
        fringe = {self.s0}
        interior = set()

        # Inicialización grafo explícito y grafo solución
        envelope_graph = Graph({self.s0: []}, self.hg.dict_state)
        bpsg = Graph({self.s0: []}, self.hg.dict_state)

        while True:
            old_policy = deepcopy(self.p)

            stack_DFS = [] # Inicializamos la pila de estados de la búsqueda "primero en profundidad"
            fringe = self.depth_first_search(envelope_graph, bpsg, self.s0, fringe, interior, stack_DFS)
            # Realizamos la búsqueda en profundidad, rellenando la pila y obteniendo el nuevo conjunto "fringe"
            self.hg.update_values(stack_DFS, self.V, self.p)
            #Actualizamos valores y política sobre los estados de la pila, según un recorrido postorden

            if all(old_policy[s] == self.p[s] for s in old_policy.keys()): # Si llegamos a convergencia, salimos del bucle
                break

    def depth_first_search(self, envelope, bpsg, i, fringe, interior, stack):
        stack.append(i) # Introducimos el estado i en la pila
        if i in fringe: # Si el estado i no hay sido aún expandido
            interior.add(i) # Lo añadimos al conjunto de estados interiores
            fringe.remove(i) # Lo eliminamos del conjunto de estados "fringe"
            fringe = fringe | set(filter(lambda s:not bpsg.dict_state[s].final and s not in interior, self.hg.get_successors(i)))
            # Actualizamos el conjunto fringe con los sucesores del estado i
            envelope.states[i] = self.hg.states[i]
            # Expandimos el estado i en el grafo "envelope"
        else: # Si el estado ha sido expandido
            for suc in self.hg.get_connector(i, self.p[i]).probs.keys(): # Para cada sucesor "greedy" del estado
                if suc not in stack and not self.hg.dict_state[suc].final: # Si el sucesor no se encuentra ya en la pila y no es un estado
                    # final
                    fringe = self.depth_first_search(envelope, bpsg, suc, fringe, interior, stack)
                    # Realizamos la llamada recursiva sobre el estado sucesor
        return fringe