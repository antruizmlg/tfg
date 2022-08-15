""" un hipergrafo está formado por un diccionario que contiene
    asociaciones (estado -> lista de conectores): se asocia cada estado
    al conjunto de k-conectores que salen de él"""
class Hipergrafo:
    def __init__(self, estados, dict_state):
        self.estados = estados
        self.dict_state = dict_state # Diccionario con asociaciones (ID de estado -> Objeto estado)

    """ Método para obtener la lista de estados sucesores de un estado en el hipergrafo"""
    def sucesores(self, s):
        list_ha = self.estados[s] # Obtenemos la lista de hiperaristas cuyo origen es el estado s.
        list_sucesores = [] # Inicializamos la lista de sucesores
        for ha in list_ha: # Para cada hiperarista de la lista
            list_sucesores += ha.destino.keys() # Concatenamos todos los estados destinos del hiperarista a la lista de sucesores
        return list(dict.fromkeys(list_sucesores)) # Devolvemos la lista de sucesores con la previa eliminación de elementos repetidos

    """ método para acutalizar el conjunto de estados 'fringe' """
    def update_fringe_set(self, F, I, s):
        for st in self.sucesores(s): # Por cada sucesor de s en el hipergrafo
            if st not in I: # Si el sucesor no se encuentra en el conjunto I
                F.add(st) # Lo introducimos en el conjunto F
        F.remove(s) # Eliminamos el estado s
        return F

    """ método para reconstruir de best partial solution graph de forma recursiva """
    def get_bpsg_states(self, envelope_graph, p, set_states, s):
        set_states.add(s) # Añadimos el estado a la lista
        best_action = p.get_politica(s) # Obtenemos la mejor acción asociada al estado (empezando por el estado inicial)
        if best_action is not None: # Si hay una mejor acción asociada a ese estado
            for ha in envelope_graph.estados[s]: # Recorremos los k-conectores que salen de ese estado
                if ha.accion == best_action: # Si el k-conector actual es el asociado con la mejor acción
                    for st in ha.destino.keys(): # Para cada uno de los estados alcanzables mediante ese k-conector
                        if st not in set_states: # Si el estado no está en la lista
                            self.get_bpsg_states(envelope_graph, p, set_states, st) # Llamamos de forma recursiva a la función para construir el árbol.
                    break
        return set_states # Devolvemos la lista de estados

    """ métodos para obtener el conjunto Z """
    def get_Z(self, envelope_graph, tablero, s, p, estados):
        predecessors = self.get_predecessors(s, tablero)
        for st in predecessors:
            if st in envelope_graph.estados.keys() and st not in estados and p.get_politica(st) is not None:
                for ha in envelope_graph.estados[st]:
                    if ha.accion == p.get_politica(st):
                        suc = ha.destino.keys()
                        break
                if s in suc:
                    estados.add(st)
                    self.get_Z(envelope_graph, tablero, st, p, estados)
        return estados

    def get_predecessors(self, s, tablero):
        sol = set()
        fila = self.dict_state[s].fila
        columna = self.dict_state[s].col

        if fila - 1 >= 0:
            sol.add(tablero[fila - 1][columna].id)
        if fila + 1 < len(tablero):
            sol.add(tablero[fila + 1][columna].id)
        if columna - 1 >= 0:
            sol.add(tablero[fila][columna - 1].id)           
        if columna + 1 < len(tablero[0]):
            sol.add(tablero[fila][columna + 1].id)

        return sol

    """ método para obtener estado no terminal """
    def no_terminal_state(self, states):
        for s in states: # Por cada estado en el conjunto states
            if not self.dict_state[s].terminal: # Si el estado no es terminal
                return s # Lo devolvemos
        return None # Si no hemos encontrado ningún estado no terminal en el conjunto, devolvemos None
    
    """ método para actualizar el hipergrafo explícito añadiendo el estado s"""
    def update_envelope_graph(self, envelope_graph, states):
        for s in states:
            envelope_graph.estados[s] = self.estados[s]

    """método que dado un hipergrafo y un conjunto de estados, obtiene la lista de predecesores del conjunto de estados en el hipergrafo"""
    def predecessor_states(self, states, I):
        sol = []
        for s in self.estados.keys():
            sucesores = self.sucesores(s)
            for suc in sucesores:
                if suc in states and s not in I:
                    sol.append(s)
                    break
        return list(dict.fromkeys(sol))

    def build_solution_graph(self, envelope_graph, s, p, estados):
        for st in envelope_graph.estados.keys(): # Para cada estado en el conjunto de estados del grafo explícito
            if not st in estados.keys(): # Si el estado no se encuentra ya en el hipergrafo Z
                for ha in envelope_graph.estados[st]: # Recorremos sus k-conectores buscando el asociado a la mejor acción del estado
                    if s in ha.destino.keys() and ha.accion == p.get_politica(st): # Si desde ese k-conector se puede alcanzar el estado s
                        # (significa que el estado st es antecesor directo del estado s) y es el k-conector asociado a la mejor acción para el estado st
                        estados[st] = ha # Lo añadimos al diccionario de estados del hipergrafo Z
                        if not s == st: # Si s es distinto a st (para evitar ciclos)
                            estados = self.build_solution_graph(envelope_graph, st, p, estados) # Llamamos de forma recursiva al método buscando 
                            # los antecesores de st que siguen la mejor política parcial para añadirlos también al hipergrafo Z
                        break
        return estados # Devolvemos el diccionario de estados asociado al hipergrafo Z.