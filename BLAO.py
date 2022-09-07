from Graph import *
from Value_Iteration import *
from copy import *

class BLAO:
    def __init__(self, hg, initial_state, final_state, h, p, problem):
        self.hg = hg # Hipergrafo
        self.s0 = initial_state.id
        self.fs = final_state.id # Estado final
        self.V = h # Función de valor inicializada con el heurístico
        self.p = p # Política inicial
        self.problem = problem
        self.table = problem.table

    def BLAO(self):
        F = {self.s0} # Conjunto fringe búsqueda hacia adelante
        I = set() # Conjunto interior. Este conjunto es compartido, los nodos se expanden buscando hacia atrás o hacia adelante.
        F_backward = {self.fs} # Conjunto fringe búsqueda hacia atrás
        
        stack_DFS = [] # Inicializamos pila búsqueda depth-first hacia adelante.
        stack_Backward = [] # Inicializamos pila búsqueda hacia atrás.

        # Inicialización grafo explícito e instancia del algoritmo iteración de valores
        envelope_graph = Graph({self.s0: [], self.fs: []}, self.hg.dict_state)
        algorithm = Value_Iteration(self.hg, self.p, self.V)
        while True:     
            F = self.hg.depth_first_search(envelope_graph, self.s0, F, I, self.p, stack_DFS)
            # Búsqueda primero en profundidad. Los nodos visitados se introducen en la pila, expandiendo los que están en el conjunto fringe
            F_backward = self.hg.backward_search(envelope_graph, self.fs, F_backward, I, self.V, self.s0, self.table, stack_DFS, stack_Backward)
            # Realizamos hacia atrás.

            self.hg.update_values(stack_DFS, self.V, self.p) # Actualizamos valores estados visitados en la búsqueda hacia adelante.
            self.hg.update_values(stack_Backward, self.V, self.p) # Actualizamos valores estados visitados en la búsqueda hacia atrás.

            #Test de convergencia
            bpsg_states = self.hg.get_bpsg_states(envelope_graph, self.p, set(), self.s0)
            algorithm.run(bpsg_states) # Aplicamos VI sobre los estados del grafo solución parcial
            bpsg_states_ = self.hg.get_bpsg_states(envelope_graph, self.p, set(), self.s0)
            if not (bpsg_states & F) and bpsg_states == bpsg_states_:        
                break