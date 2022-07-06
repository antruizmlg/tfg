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

    def interseccion(self, listaEstados):
        estadosNuevoG = [] # Inicializamos los nodos del grafo intersección
        aristasNuevoG = [] # Inicializamos las aristas del grafo intersección.
        for e in listaEstados: # Para cada nodo en la lista de nodos
            if e in self.estados: 
                estadosNuevoG.append(e) # Si el nodo está en el grafo también estará en el grafo intersección
        for ha in self.hiperaristas: # Para cada hiperarista del hipergrafo
            aristasNuevoG.append(ha.aristaConSubconjuntoDeNodos(listaEstados)) # Obtengo la hiperarista solo con los nodos en la lista de estados (intersección)
        return Hipergrafo(estadosNuevoG, aristasNuevoG)

    def obtenerEstadoNoTerminal(self):
        for e in self.estados:
            if e.esTerminal():
                return e
        return None