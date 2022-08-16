from Graph import *
from Policy_Iteration import *
from Value_Iteration import *
from copy import *
import time

class LAO:
    def __init__(self, hg, ini_state, h, pi, tablero, algorithm):
        self.hg = hg # Hipergrafo
        self.s0 = ini_state.id # Estado inicial
        self.V = h # Función de valor inicializada con el heurístico
        self.p = pi # Política inicial
        self.tablero = tablero
        self.algorithm = algorithm # Nombre del algoritmo a usar. Iteración de política o de valores.

    def LAO(self):
        # Conjuntos de estados "fringe" e "interior"
        F = {self.s0}
        I = set()

        # Inicialización grafo explícito y grafo solución
        envelope_graph = Graph({self.s0: []}, self.hg.dict_state)
        bpsg_states = {self.s0}

        # Instanciación objeto algoritmo para su posterior ejecución en cada iteración
        if self.algorithm == 'PI':
            algorithm = Policy_Iteration(self.hg, self.p, self.V) 
        if self.algorithm == 'VI':
            algorithm = Value_Iteration(self.hg, self.p, self.V)

        s = self.hg.get_no_final_state(bpsg_states & F) # Obtenemos un estado no terminal del conjunto de estados "fringe" del grafo solución
        while s is not None: # Mientras queden estados por expandir
            self.hg.update_fringe_set(F, I, s) # Actualizamos el conjunto F
            F.remove(s) # Eliminamos el estado s del conjunto fringe
            I.add(s) # Introducimos s en el conjunto I

            envelope_graph.states[s] = self.hg.states[s] # Actualizamos grafo explícito

            Z = self.hg.get_set_Z(envelope_graph, self.tablero, s, self.p, {s}) # Construimos el hipergrafo Z

            algorithm.run(Z) # Aplicamos VI o PI sobre hipergrafo Z

            bpsg_states = self.hg.get_bpsg_states(envelope_graph, self.p, set(), self.s0) # Obtenemos los estados del grafo solución

            s = self.hg.get_no_final_state(bpsg_states & F)