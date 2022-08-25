from inspect import stack
from Graph import *
from Policy_Iteration import *
from Value_Iteration import *
from copy import *
import time

class ILAO:
    def __init__(self, hg, initial_state, h, p, table):
        self.hg = hg # Hipergrafo
        self.s0 = initial_state.id # Estado inicial
        self.V = h # Función de valor inicializada con el heurístico
        self.p = p # Política inicial
        self.table = table

    def ILAO(self):
        # Conjuntos de estados "fringe" e "interior"
        fringe = {self.s0}
        interior = set()

        # Inicialización grafo explícito y grafo solución
        envelope_graph = Graph({self.s0: []}, self.hg.dict_state)

        while True:
            old_policy = deepcopy(self.p)

            stack_DFS = [] # Inicializamos la pila de estados de la búsqueda "primero en profundidad"
            fringe = self.hg.depth_first_search(envelope_graph, self.s0, fringe, interior, self.p, stack_DFS)
            # Realizamos la búsqueda en profundidad, rellenando la pila y obteniendo el nuevo conjunto "fringe"
            self.hg.update_values(stack_DFS, self.V, self.p)
            #Actualizamos valores y política sobre los estados de la pila, según un recorrido postorden

            if all(old_policy[s] == self.p[s] for s in old_policy.keys()): # Si llegamos a convergencia, salimos del bucle
                break