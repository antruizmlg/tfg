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
        bpsg = Graph({self.s0: self.hg.states[self.s0]}, self.hg.dict_state)
        expanded = set()
        fringe = set(filter(lambda s: not self.hg.dict_state[s].terminal and s not in expanded, bpsg.states.keys()))

        while fringe:
            DFS_Stack = [self.s0]
            self.depth_first_search(bpsg, self.s0, DFS_Stack)
            self.update_values(bpsg, DFS_Stack)
            self.update_bpsg(bpsg, expanded, self.s0)
            fringe = set(filter(lambda s: not self.hg.dict_state[s].terminal and s not in expanded, bpsg.states.keys()))

    def update_bpsg(self, bpsg, expanded, s):
        expanded.add(s)
        c = bpsg.get_connector(s, self.p[s])
        bpsg[s] = [c]
        for suc in c.probs.keys():
            if suc not in bpsg.states.keys() and self.p[suc] is not None:
                self.update_bpsg(bpsg, expanded, suc)

    def depth_first_search(self, bpsg, s, stack):
        if self.p[s] is not None:
            for suc in bpsg.get_connector(s, self.p[s]).probs.keys():
                stack.add(suc)
                self.depth_first_search(bpsg, suc, stack)

    def update_values(self, bpsg, stack):
        actions = {'N', 'S', 'E', 'O'}
        while stack:
            s = stack.pop()
            if not bpsg.dict_state[s].final:
                minimum = float('inf')
                for a in actions:
                    c = bpsg.get_connector(s, a)
                    val = c.cost
                    for p in c.probs.keys():
                        val += c.probs[p] * self.V[p]
                    if val < minimum:
                        minimum = val
                        best_action = a
                self.V[s] = minimum
                self.p[s] = best_action