from copy import *

class Value_Iteration:
    def __init__(self, hg, p, V):
        self.hg = hg
        self.p = p
        self.V = V

    def run(self, set):

        while True:
            oldV = deepcopy(self.V) # Almacenamos la antigua función de valor

            for s in set: # Para cada estado en el hipergrafo
                if not self.hg.dict_state[s].final: # Si el estado no es terminal
                    min_cost = float('inf') # Inicializamos menor coste encontrado
                    for c in self.hg.states[s]: # Para cada hiperarista asociada a ese estado
                        action_cost = c.cost
                        for e in c.states(): # Para cada estado destino del hiperarista
                            action_cost += c.probs[e] * oldV[e] # Sumamos la probabilidad de alcanzar el estado por el valor del estado.
                        if action_cost < min_cost: # Si ese valor (coste) es menor que el menor encontrado hasta el momento
                            min_cost = action_cost # Actualizamos el menor coste
                            best_action = c.action # Actualizamos la mejor acción
                    self.V[s] = round(min_cost, 1) # Establecemos nuevo valor asociado al estado
                    self.p[s] = best_action # Establecemos nueva mejor acción asociada al estado
                    
            if all(oldV[s] == self.V[s] for s in oldV.keys()): # Si llegamos a convergencia, salimos del bucle
                break