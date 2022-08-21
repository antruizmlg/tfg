from Graph import *
from Policy_Iteration import *
from Value_Iteration import *
from copy import *

class ILAO:
    def __init__(self, hg, initial_state, h, p, table, algorithm):
        self.hg = hg # Hipergrafo
        self.s0 = initial_state.id # Estado inicial
        self.V = h # Función de valor inicializada con el heurístico
        self.p = p # Política inicial
        self.table = table
        self.algorithm = algorithm # Nombre del algoritmo a usar. Iteración de política o de valores.

    def ILAO(self):
        while True:
            oldV = deepcopy(self.V)

            DFS_stack = self.depth_first_search()
            self.update_values(DFS_stack)

            if all(oldV[s] == self.V[s] for s in oldV.keys()): # Si llegamos a convergencia, salimos del bucle
                break

    def depth_first_search(self):
        to_expand = [self.s0]
        DFS_stack = []

        while to_expand:
            s = to_expand.pop()

            DFS_stack.append(s)
            to_expand = self.get_fringe(self.hg.get_successors(s) + to_expand, DFS_stack)

        return DFS_stack

    def get_fringe(self, list, list2):
        sol = []
        for elem in list:
            if elem not in sol and elem not in list2 and not self.hg.dict_state[elem].final:
                sol.append(elem)
        return sol

    def update_values(self, stack):
        actions = {'N', 'S', 'E', 'O'}
        while stack:
            s = stack.pop()
            if not self.hg.dict_state[s].final:
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