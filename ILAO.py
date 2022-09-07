from inspect import stack
from Graph import *
from copy import *
from Value_Iteration import *

class ILAO:
    def __init__(self, hg, initial_state, h, p, problem):
        self.hg = hg # Hipergrafo
        self.s0 = initial_state.id # Estado inicial
        self.V = h # Función de valor inicializada con el heurístico
        self.p = p # Política inicial
        self.problem = problem

    def ILAO(self):
        # Conjuntos de estados "fringe" e "interior"
        fringe = {self.s0}
        interior = set()

        envelope_graph = Graph({self.s0: []}, self.hg.dict_state)
        stack_DFS = [] # Inicializamos la pila de estados de la búsqueda "primero en profundidad"
        algorithm = Value_Iteration(self.hg, self.p, self.V)

        while True:
            fringe = self.hg.depth_first_search(envelope_graph, self.s0, fringe, interior, self.p, stack_DFS)
            # Realizamos la búsqueda en profundidad, rellenando la pila y obteniendo el nuevo conjunto "fringe"
            self.hg.update_values(stack_DFS, self.V, self.p)
            #Actualizamos valores y política sobre los estados de la pila, según un recorrido postorden
            
            #Test de convergencia
            bpsg_states = self.hg.get_bpsg_states(envelope_graph, self.p, set(), self.s0)
            algorithm.run(bpsg_states) # Aplicamos VI sobre los estados del grafo solución parcial
            bpsg_states_ = self.hg.get_bpsg_states(envelope_graph, self.p, set(), self.s0)
            if not (bpsg_states & fringe) and bpsg_states == bpsg_states_:        
                break