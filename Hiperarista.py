class Hiperarista:
    def __init__(self, src, dest, accion, coste):
        self.source = src
        self.destino = dest
        self.accion = accion
        self.coste = coste

    def aristaConSubconjuntoDeNodos(self, listaEstados):
        if not (self.source in listaEstados): # Si el nodo origen no está en la lista de nodos que queremos mantener.
            return None # El arista desaparece.
        else: # Si el nodo origen está
            dictDestino = {} # Inicializamos la lista de nodos destino y de probabilidades para cada nodo destino.
            for e in listaEstados: # Para cada elemento en la lista de estados.
                if e.id in self.destino.keys(): # Si el elemento está en la arista.
                    dictDestino[e.id] = self.destino[e.id] # Lo añadimos al diccionario con su respectiva probabilidad.
        if len(dictDestino) > 0: # Si queda algún nodo destino, devolvemos el hiperarista.
            return Hiperarista(self.source, dictDestino, self.accion, self.coste)
        else:
            return None