from copy import *

class VI:
    def __init__(self, hg, p, V):
        self.hg = hg
        self.p = p
        self.V = V

    def run(self, set):

        while True:
            oldV = deepcopy(self.V) # Almacenamos la antigua función de valor

            for s in set: # Para cada estado en el hipergrafo
                if not self.hg.dict_state[s].terminal: # Si el estado no es terminal
                    menor_coste = float('inf') # Inicializamos menor coste encontrado
                    for ha in self.hg.estados[s]: # Para cada hiperarista asociada a ese estado
                        coste_accion = ha.coste
                        for e in ha.destino.keys(): # Para cada estado destino del hiperarista
                            coste_accion += ha.destino[e] * oldV.get_valor(e) # Sumamos la probabilidad de alcanzar el estado por el valor del estado.
                        if coste_accion < menor_coste: # Si ese valor (coste) es menor que el menor encontrado hasta el momento
                            menor_coste = coste_accion # Actualizamos el menor coste
                            mejor_accion = ha.accion # Actualizamos la mejor acción
                    self.V.set_valor(s, round(menor_coste, 1)) # Establecemos nuevo valor asociado al estado
                    self.p.set_politica(s, mejor_accion) # Establecemos nueva mejor acción asociada al estado
                    
            if all(oldV.dv[s] == self.V.dv[s] for s in oldV.dv.keys()): # Si llegamos a convergencia, salimos del bucle
                break