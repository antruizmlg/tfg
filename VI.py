from copy import *

class VI:
    def __init__(self, p, V):
        self.hg = None
        self.p = p
        self.V = V

    def run(self, hg):
        self.hg = hg

        while True:
            oldV = deepcopy(self.V) # Almacenamos la antigua función de valor

            for s in self.hg.states.keys(): # Para cada estado en el hipergrafo
                menor_coste = float('inf')
                for action in self.hg.states[s].keys(): # Para cada hiperarista asociada a ese estado
                    ha = self.hg.states[s][action]
                    coste_accion = ha.coste
                    for e in ha.probs.keys(): # Para cada estado destino del hiperarista
                        coste_accion += ha.probs[e] * oldV.get_valor(e) # Sumamos la probabilidad de alcanzar el estado por el valor del estado.
                    if coste_accion < menor_coste: # Si ese valor (coste) es menor que el menor encontrado hasta el momento
                        menor_coste = coste_accion # Actualizamos el menor coste
                        mejor_accion = action
                self.V.set_valor(s, round(menor_coste, 2))
                self.p.set_politica(s, mejor_accion)

            if all(oldV.dv[s] == self.V.dv[s] for s in oldV.dv.keys()):
                break