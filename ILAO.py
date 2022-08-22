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

        while True:
            old_policy = deepcopy(self.p)

            stack_DFS = []
            fringe = self.depth_first_search(envelope_graph, bpsg, self.s0, fringe, interior, stack_DFS)
            self.hg.update_values(stack_DFS, self.V, self.p)

            if all(old_policy[s] == self.p[s] for s in old_policy.keys()): # Si llegamos a convergencia, salimos del bucle
                break

    def depth_first_search(self, envelope, bpsg, i, fringe, interior, stack):
        stack.append(i)
        if i in fringe:
            interior.add(i)
            fringe.remove(i)
            fringe = fringe | set(filter(lambda s:not bpsg.dict_state[s].final and s not in interior, self.hg.get_successors(i)))
            envelope.states[i] = self.hg.states[i]
        else:
            for suc in self.hg.get_connector(i, self.p[i]).probs.keys():
                if suc not in stack and not self.hg.dict_state[suc].final:
                    fringe = self.depth_first_search(envelope, bpsg, suc, fringe, interior, stack)
        return fringe