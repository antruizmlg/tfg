from Hipergrafo import *
from PI import *
from VI import *
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
        envelope_graph = Hipergrafo({self.s0: []}, self.hg.dict_state)
        bpsg_states = {self.s0}

        # Instanciación objeto algoritmo para su posterior ejecución en cada iteración
        if self.algorithm == 'PI':
            algorithm = PI(self.hg, self.p, self.V) 
        if self.algorithm == 'VI':
            algorithm = VI(self.hg, self.p, self.V)

        i = 0

        s = self.hg.no_terminal_state(bpsg_states & F) # Obtenemos un estado no terminal del conjunto de estados "fringe" del grafo solución
        while s is not None: # Mientras queden estados por expandir
            F = self.hg.update_fringe_set(F, I, s) # Actualizamos el conjunto F
            I.add(s) # Introducimos s en el conjunto I

            self.hg.update_envelope_graph(envelope_graph, [s]) # Actualizamos grafo explícito

            Z = self.hg.get_Z(envelope_graph, self.tablero, s, self.p, {s}) # Construimos el hipergrafo Z

            algorithm.run(Z) # Aplicamos VI o PI sobre hipergrafo Z

            bpsg_states = self.hg.get_bpsg_states(envelope_graph, self.p, set(), self.s0) # Obtenemos los estados del grafo solución

            i += 1
            s = self.hg.no_terminal_state(bpsg_states & F)

    def get_z(self, envelope_graph, s, estados):
        for st in envelope_graph.estados.keys(): # Para cada estado en el conjunto de estados del grafo explícito
            if not st in estados.keys(): # Si el estado no se encuentra ya en el hipergrafo Z
                for ha in envelope_graph.estados[st]: # Recorremos sus k-conectores buscando el asociado a la mejor acción del estado
                    if s in ha.destino.keys() and ha.accion == self.p.get_politica(st): # Si desde ese k-conector se puede alcanzar el estado s
                        # (significa que el estado st es antecesor directo del estado s) y es el k-conector asociado a la mejor acción para el estado st
                        estados[st] = envelope_graph.estados[st] # Lo añadimos al diccionario de estados del hipergrafo Z
                        if not s == st: # Si s es distinto a st (para evitar ciclos)
                            estados = self.get_z(envelope_graph, st, estados) # Llamamos de forma recursiva al método buscando 
                            # los antecesores de st que siguen la mejor política parcial para añadirlos también al hipergrafo Z
                        break
        return estados # Devolvemos el diccionario de estados asociado al hipergrafo Z.