from copy import *

class Value_Iteration:
    def __init__(self, hg, p, V, epsilon = 0.01, gamma = 1):
        self.hg = hg
        self.p = p
        self.V = V
        self.gamma = gamma
        self.epsilon = epsilon

    def run(self, set):
        it = 0

        while True:
            old_V = deepcopy(self.V)

            max_DIFF = 0
            for s in set:
                if not self.hg.dict_state[s].final:
                    max_DIFF = self.bellman_backup(s, old_V, max_DIFF)    

            it += 1
            if max_DIFF <= self.epsilon:
                self.update_policy(set)
                return it

    def bellman_backup(self, s, old_V, max_DIFF):
        min_value = float('inf') # Inicializamos menor coste encontrado
        for c in self.hg.states[s]: # Para cada hiperarista asociada a ese estado
            new_value = 0
            for e in c.states(): # Para cada estado destino del hiperarista
                new_value += c.probs[e] * old_V[e] # Sumamos la probabilidad de alcanzar el estado por el valor del estado.
            new_value = c.cost + (self.gamma * new_value)
            if new_value < min_value: # Si ese valor (coste) es menor que el menor encontrado hasta el momento
                min_value = new_value # Actualizamos el menor coste
        if abs(self.V[s] - min_value) > max_DIFF:
            max_DIFF = abs(self.V[s] - min_value)
        self.V[s] = min_value # Establecemos nuevo valor asociado al estado
        return max_DIFF

    def update_policy(self, set):
        for s in set:
            min_value = float('inf')
            for c in self.hg.states[s]:
                value = 0
                for e in c.states():
                    value += c.probs[e] * self.V[e]
                value = c.cost + (self.gamma * value)
                if value < min_value:
                    min_value = value
                    self.p[s] = c.action