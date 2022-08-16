""" un hipergrafo está formado por un diccionario que contiene
    asociaciones (estado -> lista de conectores): se asocia cada estado
    al conjunto de k-conectores que salen de él"""
class Graph:
    def __init__(self, states, dict_state):
        self.states = states
        self.dict_state = dict_state # Diccionario con asociaciones (ID de estado -> Objeto estado)

    """ Método para obtener la lista de estados sucesores de un estado en el hipergrafo"""
    def successors(self, s):
        suc = [] # Inicializamos la lista de sucesores
        for c in self.states[s]: # Para cada hiperarista de la lista
            suc += c.states() # Concatenamos todos los estados destinos del hiperarista a la lista de sucesores
        return suc # Devolvemos la lista de sucesores con la previa eliminación de elementos repetidos

    """ método para acutalizar el conjunto de estados 'fringe' """
    def update_fringe_set(self, F, I, s):
        for st in self.successors(s): # Por cada sucesor de s en el hipergrafo
            if st not in I: # Si el sucesor no se encuentra en el conjunto I
                F.add(st) # Lo introducimos en el conjunto F

    """ método para reconstruir de best partial solution graph de forma recursiva """
    def get_bpsg_states(self, graph, p, set_states, s):
        set_states.add(s) # Añadimos el estado a la lista
        best_action = p[s] # Obtenemos la mejor acción asociada al estado (empezando por el estado inicial)
        if best_action is not None: # Si hay una mejor acción asociada a ese estado
            for st in self.get_connector(s, best_action).states(): # Por cada estado sucesor de esa acción en el grafo
                if st not in set_states: # Si el estado no está en la lista
                    self.get_bpsg_states(graph, p, set_states, st) # Llamamos de forma recursiva a la función para construir el árbol.
        return set_states # Devolvemos la lista de estados

    """ métodos para obtener el conjunto Z """
    def get_set_Z(self, envelope_graph, table, s, p, Z):
        predecessors = self.get_predecessors(s, table)
        for st in predecessors:
            if st in envelope_graph.states and st not in Z and p[st] is not None:
                suc = self.get_connector(st, p[st]).states()
                if s in suc:
                    Z.add(st)
                    self.get_set_Z(envelope_graph, table, st, p, Z)
        return Z

    def get_predecessors(self, s, table):
        sol = set()
        row = self.dict_state[s].row
        col = self.dict_state[s].col

        if row - 1 >= 0:
            sol.add(table[row - 1][col].id)
        if row + 1 < len(table):
            sol.add(table[row + 1][col].id)
        if col - 1 >= 0:
            sol.add(table[row][col - 1].id)           
        if col + 1 < len(table[0]):
            sol.add(table[row][col + 1].id)

        return sol

    """ método para obtener estado no terminal """
    def get_no_final_state(self, states):
        for s in states: # Por cada estado en el conjunto states
            if not self.dict_state[s].final: # Si el estado no es terminal
                return s # Lo devolvemos
        return None # Si no hemos encontrado ningún estado no terminal en el conjunto, devolvemos None
    
    """método que dado un estado, devuelve el conector asociado a la acción dada"""
    def get_connector(self, state, action):
        for c in self.states[state]:
            if c.action == action:
                break
        return c