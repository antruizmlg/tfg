from Hipergrafo import *
from PI import *
from VI import *
from copy import *

class LAO:
    def __init__(self, est_id, hg, ini_state, h, pi, algorithm):
        self.estado_por_id = est_id
        self.hg = hg
        self.s0 = ini_state.id
        self.h = h
        self.pi = pi
        self.algorithm = algorithm

    def LAO(self):
        V = self.h
        F = [self.s0]
        I = []
        envelope_graph = Hipergrafo([self.s0], [])
        bpsg = deepcopy(envelope_graph)
        s = self.get_estado_no_terminal(list(set(bpsg.estados) & set(F)))
        while s is not None:
            F = self.update_fringe_set(F, I, s)
            I.append(s) # Introducimos s en el conjunto I
            envelope_graph = self.update_envelope_graph(self.hg, I, F)
            Z = self.get_Z() # Construimos el conjunto Z
            if self.algorithm == 'PI':
                pi_algorithm = PI(Z, self.pi, V) 
                pi_algorithm.policy_iterations() # Iteración de políticas sobre el conjunto Z
            else:
                vi_algorithm = VI(Z, self.politica, V) 
                vi_algorithm.value_iteration() # Iteración de políticas sobre el conjunto Z
            bpsg = self.rebuild(envelope_graph, self.politica)
            s = self.get_estado_no_terminal(list(set(bpsg.estados) & set(F)))
        return self.politica, V

    def update_fringe_set(self, F, I, s):
        for estado in self.hg.sucesores(s): # Por cada sucesor de s en el hipergrafo
            if estado not in I: # Si el sucesor no se encuentra en el conjunto I
                F.append(estado) # Lo introducimos en el conjunto F
        F = list(dict.fromkeys(F)) # Eliminamos los elementos repetidos
        F.remove(s) # Eliminamos el estado s
        return F

    def rebuild(self, envelope_graph, politica):
        listaNodos = [] # Inicializamos la lista de nodos del hipergrafo.
        listaAristas = [] # Inicializamos la lista de aristas del hipergrafo.
        for ha in envelope_graph.hiperaristas: # Para cada arista
            if ha.accion == politica.getPolitica(ha.source.id): # Si la acción de la arista coincide con la dictada por la política
                listaNodos.append(ha.source) # Introducimos el nodo en la lista de nodos.
                listaAristas.append(ha) # Introducimos la arista en la lista de aristas.
                for estado in ha.destino.keys():
                    listaNodos.append(self.hg.estados[estado])
        listaNodos = list(dict.fromkeys(listaNodos))
        return Hipergrafo(listaNodos, listaAristas)

    def get_Z(self):
        return None
    
    @staticmethod
    def update_envelope_graph(hg, I, F):
        listaNodos = I + F # Unión de las listas I y F.
        listaAristas = [] # Inicializo la lista de aristas vacía
        for arista in hg.hiperaristas: # Para cada arista del hipergrafo original
            ha = arista.aristaConSubconjuntoDeNodos(listaNodos) # Elimino de la arista los estados que no se encuentren en la lista de nodos.
            if ha is not None: # Si la arista no ha sido descartada al considerar solo los estados en la lista de nodos.
                if ha.source in I: # Si el origen de la arista está en el conjunto I (Los nodos F no han sido expandidos por lo que no se tiene en cuenta)
                    listaAristas.append(ha) # Añadimos la arista al conjunto de aristas
        return Hipergrafo(listaNodos, listaAristas)

    @staticmethod
    def get_estado_no_terminal(l):
        for e in l:
            if not e.esTerminal():
                return e
        return None