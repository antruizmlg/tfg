class Hipergrafo:
    def __init__(self, estados, hiperaristas):
        self.estados = estados
        self.hiperaristas = hiperaristas

    def sucesores(self, estado):
        sucesores = [] # Inicializamos la lista de sucesores
        for a in self.hiperaristas: # Por cada hiperarista del hipergrafo.
            if a.source == estado: # Si el origen de la hiperarista coincide con el estado
                for elem in a.destino.keys():
                    sucesores.append(elem) # Introducimos en la lista de sucesores todos los nodos destinos del hiperarista.
        return list(dict.fromkeys(sucesores)) # Devolvemos la lista de sucesores sin elementos repetidos