from copy import *

class Value_Iteration:
    def __init__(self, hg, p, V, p_convergence = False):
        self.hg = hg
        self.p = p
        self.V = V
        self.p_convergence = p_convergence

    def run(self, set):
        while True:
            old_V = deepcopy(self.V)
            old_p = deepcopy(self.p)
            self.bellman_backup(set, old_V)
            if self.test_convergence(old_V, old_p):
                break

    def bellman_backup(self, set, old_V):
        for s in set: # Para cada estado en el hipergrafo
            if not self.hg.dict_state[s].final: # Si el estado no es terminal
                best_action = None
                min_cost = float('inf') # Inicializamos menor coste encontrado
                for c in self.hg.states[s]: # Para cada hiperarista asociada a ese estado
                    action_cost = c.cost
                    for e in c.states(): # Para cada estado destino del hiperarista
                        action_cost += c.probs[e] * old_V[e] # Sumamos la probabilidad de alcanzar el estado por el valor del estado.
                    if action_cost < min_cost: # Si ese valor (coste) es menor que el menor encontrado hasta el momento
                        min_cost = action_cost # Actualizamos el menor coste
                        best_action = c.action # Actualizamos la mejor acción
                self.V[s] = round(min_cost, 2) # Establecemos nuevo valor asociado al estado
                self.p[s] = best_action # Establecemos nueva mejor acción asociada al 
                
    def test_convergence(self, old_V, old_p):
        if self.p_convergence:
            return all(old_p[s] == self.p[s] for s in old_p.keys())
        else:
            all(old_V[s] == self.V[s] for s in old_V.keys())