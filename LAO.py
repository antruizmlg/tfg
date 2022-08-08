from Hipergrafo import *
from PI import *
from VI import *
from copy import *

class LAO:
    def __init__(self, dict_state, hg, ini_state, h, pi, algorithm):
        self.dict_state = dict_state # Diccionario con asociaciones (ID de estado -> Objeto estado)
        self.hg = hg # Hipergrafo
        self.s0 = ini_state.id # Estado inicial
        self.V = h # Función de valor inicializada con el heurístico
        self.p = pi # Política inicial
        self.algorithm = algorithm # Nombre del algoritmo a usar. Iteración de política o de valores.

    def LAO(self):
        # Conjuntos de estados "fringe" e "interior"
        F = [self.s0]
        I = []

        # Listas para almacenar el tamaño del grafo explícito, el grafo solución y el hipergrafo Z
        Z_percent = []
        Z_sizes = []

        # Inicialización grafo explícito y grafo solución
        envelope_graph = Hipergrafo({self.s0: []})
        bpsg = deepcopy(envelope_graph)

        # Instanciación objeto algoritmo para su posterior ejecución en cada iteración
        if self.algorithm == 'PI':
            algorithm = PI(self.p, self.V, self.dict_state) 
        if self.algorithm == 'VI':
            algorithm = VI(self.p, self.V, self.dict_state)

        s = self.no_terminal_state(list(set(bpsg.estados) & set(F))) # Obtenemos un estado no terminal del conjunto de estados "fringe" del grafo solución
        while s is not None: # Mientras queden estados por expandir
            F = self.update_fringe_set(F, I, s) # Actualizamos el conjunto F
            I.append(s) # Introducimos s en el conjunto I

            envelope_graph = self.update_envelope_graph(envelope_graph, s) # Actualizamos grafo explícito
            Z = Hipergrafo(self.get_z(envelope_graph, s, {s:envelope_graph.estados[s]})) # Construimos el hipergrafo Z 

            algorithm.run(Z) # Aplicamos VI o PI sobre hipergrafo Z
            bpsg = Hipergrafo(self.rebuild(envelope_graph, {}, self.s0)) # Reconstruimos el "best partian solution graph" 

            # Añadimos los tamaños de los hipergrafos a sus respectivas listas
            Z_percent.append(len(Z.estados)/len(self.hg.estados)*100)
            Z_sizes.append(len(Z.estados))

            s = self.no_terminal_state(list(set(bpsg.estados) & set(F)))
            
        return Z_sizes, Z_percent # Devolvemos tamaños de los hipergrafos en cada iteración

    """ método para acutalizar el conjunto de estados 'fringe' """
    def update_fringe_set(self, F, I, s):
        for st in self.hg.sucesores(s): # Por cada sucesor de s en el hipergrafo
            if st not in I: # Si el sucesor no se encuentra en el conjunto I
                F.append(st) # Lo introducimos en el conjunto F
        F = list(dict.fromkeys(F)) # Eliminamos los elementos repetidos
        F.remove(s) # Eliminamos el estado s
        return F

    """ método para reconstruir de best partial solution graph de forma recursiva """
    def rebuild(self, envelope_graph, dict, s):
        best_action = self.p.get_politica(s) # Obtenemos la mejor acción asociada al estado (empezando por el estado inicial)
        if best_action is not None: # Si hay una mejor acción asociada a ese estado
            for ha in envelope_graph.estados[s]: # Recorremos los k-conectores que salen de ese estado
                if ha.accion == best_action and s not in dict.keys(): # Si el k-conector actual es el asociado con la mejor acción
                    # y s no está ya en el grafo.
                    dict[s] = [ha] # Añadimos s al grafo con el k-conector asociado a su mejor acción
                    for st in ha.destino.keys(): # Para cada uno de los estados alcanzables mediante ese k-conector
                        dict = self.rebuild(envelope_graph, dict, st) # Llamamos de forma recursiva a la función para construir el árbol.
        elif s not in dict.keys(): # De lo contrario, si el estado no tiene asociado una mejor acción y no está ya en el grafo solución,
            # significa que estamos ante un nodo "hoja", es decir, un nodo que todavía no ha sido expandido.
                dict[s] = [] # Lo añadimos al diccionario del grafo solución sin k-conectores
        return dict # Devolvemos el diccionario

    """ método para obtener hipergrafo Z de forma recursiva """
    def get_z(self, envelope_graph, s, estados):
        for st in envelope_graph.estados.keys(): # Para cada estado en el conjunto de estados del grafo explícito
            if not st in estados.keys(): # Si el estado no se encuentra ya en el hipergrafo Z
                for ha in envelope_graph.estados[st]: # Recorremos sus k-conectores buscando el asociado a la mejor acción del estado
                    if s in ha.destino.keys() and ha.accion == self.p.get_politica(st): # Si desde ese k-conector se puede alcanzar el estado s
                        # (significa que el estado st es antecesor directo del estado s) y es el k-conector asociado a la mejor acción para el estado st
                        estados[st] = envelope_graph.estados[st] # Lo añadimos al diccionario de estados del hipergrafo Z
                        if not s == st: # Si s es distinto a st (para evitar ciclos)
                            estados = self.get_z(envelope_graph, st, estados) # Llamamos de forma recursiva al método buscando 
                            # los antecesores de st que siguen la mejor política parcial para añadirlos también al hipergrafo Z
                        break
        return estados # Devolvemos el diccionario de estados asociado al hipergrafo Z.

    """ método para obtener estado no terminal """
    def no_terminal_state(self, states):
        for s in states: # Por cada estado en el conjunto states
            if not self.dict_state[s].terminal: # Si el estado no es terminal
                return s # Lo devolvemos
        return None # Si no hemos encontrado ningún estado no terminal en el conjunto, devolvemos None
    
    """ método para actualizar el hipergrafo explícito añadiendo el estado s"""
    def update_envelope_graph(self, envelope_graph, s):
        envelope_graph.estados[s] = self.hg.estados[s]
        return envelope_graph