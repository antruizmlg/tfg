from Graph import *
from Policy_Iteration import *
from Value_Iteration import *
from copy import *

class BLAO:
    def __init__(self, hg, initial_state, final_state, h, p, table, algorithm):
        self.hg = hg # Hipergrafo
        self.s0 = initial_state.id
        self.fs = final_state.id # Estado final
        self.V = h # Función de valor inicializada con el heurístico
        self.p = p # Política inicial
        self.table = table
        self.algorithm = algorithm # Nombre del algoritmo a usar. Iteración de política o de valores.

    def BLAO(self):
        # Conjuntos de estados "fringe" e "interior"
        F = {self.s0}
        I = set()

        F_Reverse = {self.fs}
        I_reverse = set()

        forward_graph = Graph({self.s0: []}, self.hg.dict_state)
        reverse_graph = Graph({self.fs: []}, self.hg.dict_state)
        bpsg_states = {self.s0}

        overlapped = False

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
            forward_graph.states[s] = self.hg.states[s] # Actualizamos grafo explícito

            for state in F_Reverse:
                reverse_graph.states[state] = self.hg.states[state]     
            I_reverse = I_reverse | F_Reverse
            F_Reverse = self.hg.update_fringe_rlao(self.table, F_Reverse, I_reverse)  

            if not overlapped and (set(reverse_graph.states.keys()) | set(forward_graph.states.keys())):
                forward_graph.states.update(reverse_graph.states)
                F = F | F_Reverse
                overlapped = True

            Z = self.hg.get_set_Z(forward_graph, self.table, s, self.p, {s})
            algorithm.run(Z)

            if not overlapped:
                algorithm.run(reverse_graph.states.keys())

            bpsg_states = self.hg.get_bpsg_states(forward_graph, self.p, set(), self.s0)
            s = self.hg.get_no_final_state(bpsg_states & F)            