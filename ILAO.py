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
        bpsg_states = filter(lambda s:not bpsg.dict_state[s].terminal, bpsg.states.keys())

        # Instanciación objeto algoritmo para su posterior ejecución en cada iteración
        if self.algorithm == 'PI':
            algorithm = Policy_Iteration(self.hg, self.p, self.V) 
        if self.algorithm == 'VI':
            algorithm = Value_Iteration(self.hg, self.p, self.V)

        while fringe & bpsg_states:
            stack_DFS = []
            self.depth_first_search(envelope_graph, bpsg, self.s0, fringe, interior, stack_DFS)
            self.update_values(bpsg, stack_DFS)
            algorithm.run(bpsg.states.keys())
            bpsg_states = self.hg.get_bpsg_states(envelope_graph, self.p, set(), self.s0)

    def depth_first_search(self, envelope, bpsg, i, fringe, interior, stack):
        stack.append(suc)
        if i in fringe:
            interior.add(i)
            fringe.remove(i)
            fringe = fringe + filter(lambda s:not bpsg.dict_state[s].terminal and s not in interior, self.hg.get_successors(i))
            envelope.states[i] = self.hg.states[i]
        else:
            for suc in bpsg.get_connector(i, self.p[i]).probs.keys():
                self.depth_first_search(bpsg, suc, stack)

    def update_values(self, bpsg, stack):
        actions = {'N', 'S', 'E', 'O'}
        while stack:
            s = stack.pop()
            if not bpsg.dict_state[s].final:
                minimum = float('inf')
                for a in actions:
                    c = self.hg.get_connector(s, a)
                    val = c.cost
                    for p in c.probs.keys():
                        val += c.probs[p] * self.V[p]
                    if val < minimum:
                        minimum = val
                        best_action = a
                self.V[s] = minimum
                self.p[s] = best_action