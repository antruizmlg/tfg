from copy import *

class VI:
    def __init__(self, hipergrafo, politica, V):
        self.hipergrafo = hipergrafo
        self.politica = politica
        self.V = V

    def value_iteration(self):
        estados = list(self.politica.politica.keys()) # Inicializamos una lista con todos los estados
        mejor_accion_actual = list(self.politica.politica.values())  # Inicializamos una lista que almacenará la mejor política encontrada para cada estado en un momento determinado

        while True:
            oldV = deepcopy(self.V) # Almacenamos la antigua función de valor

            for ha in self.hipergrafo.hiperaristas: # Para cada arista en el conjunto de aristas del grafo.
                i = estados.index(ha.source.id) # Obtenemos el índice en la lista de estados
                valor_ha = ha.coste
                for e in ha.destino.keys():
                    valor_ha += ha.destino[e] * oldV.getValor(e) # Calculamos el valor de realizar la acción de la hiperarista desde ese estado.
                if valor_ha < self.V.getValor(ha.source.id): # Si ese valor (coste) es menor que el menor encontrado hasta el momento
                    self.V.setValor(ha.source.id, valor_ha) # Actualizamos el menor valor
                    mejor_accion_actual[i] = ha.accion # Actualizamos la mejor política

            if all(oldV.dv[s] == self.V.dv[s] for s in oldV.dv.keys()):
                break

        for ind in range(len(estados)): # Recorremos la lista de estado.
            self.politica.politica[estados[ind]] = mejor_accion_actual[ind]  # Actualizamos la política: para cada estado, almacenamos su mejor acción en el diccionario.