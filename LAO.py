from Hipergrafo import *
from PI import *

class LAO:
    def __init__(self, hipergrafo, estadoInicial, heuristico, politica):
        self.hipergrafo = hipergrafo
        self.eIni = estadoInicial
        self.heuristico = heuristico
        self.politica = politica

    def LAO(self):
        V = self.heuristico
        F = [self.eIni]
        I = []
        G = Hipergrafo([self.eIni], None)
        GV = Hipergrafo([self.eIni], None)
        s = self.hipergrafo.interseccion(F).obtenerEstadoNoTerminal()
        while s is not None:
            F.remove(s) # Eliminamos el estado s
            for estado in self.hipergrafo.sucesores(s): # Por cada sucesor de s en el hipergrafo
                if estado not in I: # Si el sucesor no se encuentra en el conjunto I
                    F.append(estado) # Lo introducimos en el conjunto F
            I.append(s) # Introducimos s en el conjunto I
            G = self.update_envelope_graph(self.hipergrafo, I, F)
        policy_algorithm = PI(GV, self.politica, V)
        PI.policy_iterations()
        GV = self.rebuild(G, self.politica)
        s = self.hipergrafo.interseccion(F).obtenerEstadoNoTerminal()
        return self.politica, V
    
    @staticmethod
    def update_envelope_graph(hipergrafo, I, F):
        listaNodos = I + F # Unión de las listas I y F. No es necesario eliminar elementos repetidos.
        listaAristas = [] # Inicializo la lista de aristas vacía
        for arista in hipergrafo.hiperaristas: # Para cada arista del hipergrafo original
            ha = arista.aristaConSubconjuntoDeNodos(listaNodos) # Elimino de la arista los estados que no se encuentren en la lista de nodos.
            if ha is not None: # Si la arista no ha sido descartada al considerar solo los estados en la lista de nodos.
                if ha.source in I: # Si el origen de la arista está en el conjunto I (Los nodos F no han sido expandidos por lo que no se tiene en cuenta)
                    listaAristas.append(ha) # Añadimos la arista al conjunto de aristas
        return Hipergrafo(listaNodos, listaAristas)

    @staticmethod
    def rebuild(G, politica):
        listaNodos = [] # Inicializamos la lista de nodos del hipergrafo.
        listaAristas = [] # Inicializamos la lista de aristas del hipergrafo.
        for ha in G.hiperaristas: # Para cada arista
            if ha.accion == politica.getPolitica(ha.source): # Si la acción de la arista coincide con la dictada por la política
                listaNodos.append(ha.source) # Introducimos el nodo en la lista de nodos.
                listaAristas.append(ha) # Introducimos la arista en la lista de aristas.
        return Hipergrafo(listaNodos, listaAristas)