from copy import *

class VI:
    def __init__(self, hg, p, V):
        self.hg = hg
        self.p = p
        self.V = V

    def value_iteration(self):
        while True:
            oldV = deepcopy(self.V) # Almacenamos la antigua función de valor

            for s in self.hg.estados.keys(): # Para cada estado en el hipergrafo
                menor_coste = float('inf')
                mejor_accion = self.p.get_politica(s)
                for ha in self.hg.estados[s]: # Para cada hiperarista asociada a ese estado
                    coste_accion = ha.coste
                    for e in ha.destino.keys(): # Para cada estado destino del hiperarista
                        coste_accion += ha.destino[e] * oldV.get_valor(e) # Sumamos la probabilidad de alcanzar el estado por el valor del estado.
                    if coste_accion < menor_coste: # Si ese valor (coste) es menor que el menor encontrado hasta el momento
                        menor_coste = coste_accion # Actualizamos el menor coste
                        mejor_accion = ha.accion
                self.V.set_valor(s, round(menor_coste, 2))
                self.p.set_politica(s, mejor_accion)

            if all(oldV.dv[s] == self.V.dv[s] for s in oldV.dv.keys()):
                break