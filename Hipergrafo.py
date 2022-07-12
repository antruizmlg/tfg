class Hipergrafo:
    def __init__(self, estados):
        self.estados = estados

    def sucesores(self, s):
        list_ha = self.estados[s] # Obtenemos la lista de hiperaristas cuyo origen es el estado s.
        list_sucesores = [] # Inicializamos la lista de sucesores
        for ha in list_ha: # Para cada hiperarista de la lista
            list_sucesores += ha.destino.keys() # Concatenamos todos los estados destinos del hiperarista a la lista de sucesores
        return list(dict.fromkeys(list_sucesores)) # Devolvemos la lista de sucesores con la previa eliminación de elementos repetidos