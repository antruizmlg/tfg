from Graph import *
from Value_Iteration import *
from copy import *

class LAO:
    def __init__(self, hg, ini_state, h, pi, problem):
        self.hg = hg # Hipergrafo
        self.s0 = ini_state.id # Estado inicial
        self.V = h # Función de valor inicializada con el heurístico
        self.p = pi # Política inicial
        self.table = problem.table
        self.problem = problem

    def LAO(self):
        # Conjuntos de estados "fringe" e "interior"
        fringe = {self.s0}
        interior = set()

        # Inicialización grafo explícito
        explicit_graph = Graph({self.s0: []}, self.hg.dict_state)
        bpsg_states = {self.s0}

        # Instanciación objeto algoritmo para su posterior ejecución en cada iteración
        algorithm = Value_Iteration(self.hg, self.p, self.V)

        while True: # Mientras queden estados por expandir
            while bpsg_states & fringe:
                # Estado s a expandir
                s = (bpsg_states & fringe).pop()
                # Eliminamos s de fringe
                fringe.remove(s)
                interior.add(s) # Introducimos s en el conjunto I
                # Introducimos en F sucesores de s que no sean interiores
                fringe = fringe | set(filter(lambda s: s not in interior, self.hg.get_successors(s)))
                explicit_graph.states[s] = self.hg.states[s] # Actualizamos grafo explícito
                Z = self.hg.set_Z(explicit_graph, self.table, s, self.p, {s}) # Obtenemos estados conjunto Z
                algorithm.run(Z) # Aplicamos VI sobre estados en Z
                bpsg_states = self.hg.get_bpsg_states(self.p, set(), self.s0) # Obtenemos estados del grafo solución parcial

            # Test de convergencia
            algorithm.run(bpsg_states)
            bpsg_states = self.hg.get_bpsg_states(self.p, set(), self.s0)
            if not (bpsg_states & fringe): # Si llegamos a convergencia, salimos del bucle
                return bpsg_states