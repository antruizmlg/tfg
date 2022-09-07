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
        F = {self.s0}
        I = set()

        # Inicialización grafo explícito
        envelope_graph = Graph({self.s0: []}, self.hg.dict_state)
        bpsg_states = {self.s0}

        # Instanciación objeto algoritmo para su posterior ejecución en cada iteración
        algorithm = Value_Iteration(self.hg, self.p, self.V)

        while True: # Mientras queden estados por expandir
            s = (bpsg_states & F).pop()
            self.hg.update_fringe_set(F, I, s) # Actualizamos el conjunto F
            F.remove(s)
            I.add(s) # Introducimos s en el conjunto I
            envelope_graph.states[s] = self.hg.states[s] # Actualizamos grafo explícito

            Z = self.hg.get_set_Z(envelope_graph, self.table, s, self.p, {s}) # Obtenemos estados conjunto Z
            algorithm.run(Z) # Aplicamos VI sobre estados en Z

            #Test de convergencia
            algorithm.run(self.hg.get_bpsg_states(envelope_graph, self.p, set(), self.s0)) # Aplicamos VI sobre los estados del grafo solución parcial
            bpsg_states = self.hg.get_bpsg_states(envelope_graph, self.p, set(), self.s0)
            if not (bpsg_states & F): # Si llegamos a convergencia, salimos del bucle
                break