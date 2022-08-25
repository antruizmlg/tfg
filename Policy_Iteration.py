from copy import *
import random

class Policy_Iteration:
    def __init__(self, hg, p, V):
        self.set = None
        self.hg = hg
        self.p = p
        self.V = V

    def run(self, set):
        self.set = set

        for s in set:
            self.p[s] = 'N'

        while True:
            old_policy = deepcopy(self.p) # Hacemos una copia de la política actual

            self.policy_evaluation() # Modificamos la función de valor mediante evaluación de la política

            self.policy_improvement() # Obtenemos la mejor política con la nueva función de valor

            if all(old_policy[s] == self.p[s] for s in old_policy.keys()): # Si la nueva política coincide con la anterior, hemos llegado a una convergencia.
                break

    def policy_evaluation(self):
        while True:
            oldV = deepcopy(self.V) # Almacenamos la antigua función de valor

            for s in self.set: # Para cada estado
                if not self.hg.dict_state[s].final: # Si el estado no es terminal
                    c = self.hg.get_connector(s, self.p[s])
                    new_value = c.cost
                    for st in c.states(): # Para cada estado destino
                        new_value += c.probs[st] * oldV[st] # Sumamos la probabilidad de alcanzar ese estado desde el actual por el valor de ese estado
                    self.V[s] = new_value # Modificamos el nuevo valor del estado actual.

            if all(oldV[s] == self.V[s] for s in oldV.keys()): # Si llegamos a convergencia, salimos del bucle
                break

    def policy_improvement(self):
        for s in self.set: # Para cada estado del grafo.
            if not self.hg.dict_state[s].final:
                min_cost = float('inf')
                for c in self.hg.states[s]: # Para cada hiperarista asociada a ese estado.
                    action_cost = c.cost
                    for e in c.states(): # Para cada estado alcanzable mediante la acción
                        action_cost += c.probs[e] * self.V[e] # Sumamos la probabilidad de alcanzar el estado por el valor del estado.
                    if action_cost < min_cost: # Si el coste de la acción es menor que el minimo encontrado hasta el momento
                        best_action = c.action # Actualizamos la mejor acción hasta el momento
                        min_cost = action_cost # Actualizamos el mínimo coste encontrado hasta el momento
                self.p[s] = best_action # Actualizamos la política con la mejor acción