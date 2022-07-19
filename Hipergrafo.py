class Hipergrafo:
    def __init__(self, states):
        self.states = states

    def sucesores(self, s):
        list_ha = list(self.states[s].values()) # Obtenemos la lista de hiperaristas cuyo origen es el estado s.
        list_sucesores = [] # Inicializamos la lista de sucesores
        for ha in list_ha: # Para cada hiperarista de la lista
            list_sucesores += ha.probs.keys() # Concatenamos todos los estados destinos del hiperarista a la lista de sucesores
        return list(dict.fromkeys(list_sucesores)) # Devolvemos la lista de sucesores con la previa eliminación de elementos repetidos