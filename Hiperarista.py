class Hiperarista:
    def __init__(self, src, dest, probabilidades, accion, coste):
        self.source = src
        self.destino = dest
        self.prob = probabilidades
        self.accion = accion
        self.coste = coste

    def aristaConSubconjuntoDeNodos(self, listaEstados):
        if not (self.source in listaEstados): # Si el nodo origen no está en la lista de nodos que queremos mantener.
            return None # El arista desaparece.
        else: # Si el nodo origen está
            listaDestino = []
            listaProb = [] # Inicializamos la lista de nodos destino y de probabilidades para cada nodo destino.
            for e in listaEstados: # Para cada elemento en la lista de estados.
                if e in self.destino: # Si el elemento está en la arista.
                    i = self.destino.index(e)
                    listaDestino.append(self.destino[i])
                    listaProb.append(self.prob[i])
        if len(listaDestino) > 0:
            return Hiperarista(self.source, listaDestino, listaProb, self.accion, self.coste)
        else:
            return None