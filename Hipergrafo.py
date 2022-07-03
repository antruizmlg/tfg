class Hipergrafo:
    def __init__(self, estados, hiperaristas):
        self.estados = estados
        self.hiperaristas = hiperaristas

    def interseccion(self, listaEstados):
        estadosNuevoG = [] # Inicializamos los nodos del grafo intersección
        aristasNuevoG = [] # Inicializamos las aristas del grafo intersección.
        for e in listaEstados: # Para cada nodo en la lista de nodos
            if e in self.estados: 
                estadosNuevoG.append(e) # Si el nodo está en el grafo también estará en el grafo intersección
        for ha in self.hiperaristas: # Para cada hiperarista del hipergrafo
            aristasNuevoG.append(ha.aristaConSubconjuntoDeNodos(listaEstados)) # Obtengo la hiperarista solo con los nodos en la lista de estados (intersección)
        return Hipergrafo(estadosNuevoG, aristasNuevoG)