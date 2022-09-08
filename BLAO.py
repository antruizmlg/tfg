from Graph import *
from Value_Iteration import *
from copy import *

class BLAO:
    def __init__(self, hg, initial_state, final_state, h, p, problem):
        self.hg = hg # Hipergrafo
        self.s0 = initial_state.id
        self.fs = final_state.id # Estado final
        self.V = h # Función de valor inicializada con el heurístico
        self.p = p # Política inicial
        self.problem = problem
        self.table = problem.table

    def BLAO(self):
        bpsg = Graph({self.s0:[]}, self.hg.dict_state)
        explicit_graph = deepcopy(bpsg)

        algorithm = Value_Iteration(self.hg, self.p, self.V)

        expanded = set()
        unexpanded = set(filter(lambda s: not s in expanded and not bpsg.dict_state[s].final, bpsg.states.keys()))
        while True:
            old_p = deepcopy(self.p)

            while unexpanded:
                s = unexpanded.pop()

                if not s in expanded and not bpsg.dict_state[s].final:
                    expanded.add(s)
                    explicit_graph.states[s] = self.hg.states[s]
                    self.hg.update_values([s], self.V, self.p)               
                bpsg_states = self.hg.get_bpsg_states(explicit_graph, self.p, set(), self.s0)

            Z = [s for s in bpsg_states if not bpsg.dict_state[s].final]
            algorithm.run(Z)
            
            if all(old_p[s] == self.p[s] for s in old_p.keys()): 
                break

            bpsg_states = self.hg.get_bpsg_states(explicit_graph, self.p, set(), self.s0)
            unexpanded = set(filter(lambda s: s not in expanded and not bpsg.dict_state[s].final, bpsg_states))     