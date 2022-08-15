from Hipergrafo import *
from PI import *
from VI import *
from copy import *
import time

class LAO:
    def __init__(self, hg, ini_state, h, pi, algorithm):
        self.hg = hg # Hipergrafo
        self.s0 = ini_state.id # Estado inicial
        self.V = h # Función de valor inicializada con el heurístico
        self.p = pi # Política inicial
        self.algorithm = algorithm # Nombre del algoritmo a usar. Iteración de política o de valores.

    def LAO(self):
        # Conjuntos de estados "fringe" e "interior"
        F = [self.s0]
        I = []

        # Inicialización grafo explícito y grafo solución
        envelope_graph = Hipergrafo({self.s0: []}, self.hg.dict_state)
        bpsg_states = [self.s0]

        # Instanciación objeto algoritmo para su posterior ejecución en cada iteración
        if self.algorithm == 'PI':
            algorithm = PI(self.p, self.V) 
        if self.algorithm == 'VI':
            algorithm = VI(self.hg, self.p, self.V)

        s = self.hg.no_terminal_state(list(set(bpsg_states) & set(F))) # Obtenemos un estado no terminal del conjunto de estados "fringe" del grafo solución
        while s is not None: # Mientras queden estados por expandir
            F = self.hg.update_fringe_set(F, I, s) # Actualizamos el conjunto F
            I.append(s) # Introducimos s en el conjunto I

            self.hg.update_envelope_graph(envelope_graph, [s]) # Actualizamos grafo explícito
            Z = self.hg.set_Z(envelope_graph, s, self.p, [s]) # Construimos el hipergrafo Z

            algorithm.run(Z) # Aplicamos VI o PI sobre hipergrafo Z

            bpsg_states = self.hg.get_bpsg_states(envelope_graph, self.p, [], self.s0) # Obtenemos los estados del grafo solución

            s = self.hg.no_terminal_state(list(set(bpsg_states) & set(F)))