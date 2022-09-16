""" un hipergrafo está formado por un diccionario que contiene
    asociaciones (estado -> lista de conectores): se asocia cada estado
    al conjunto de k-conectores que salen de él"""
class Graph:
    def __init__(self, states, dict_state):
        self.states = states
        self.dict_state = dict_state # Diccionario con asociaciones (ID de estado -> Objeto estado)

    """ Método para obtener la lista de estados sucesores de un estado en el hipergrafo"""
    def get_successors(self, s):
        suc = [] # Inicializamos la lista de sucesores
        for c in self.states[s]: # Para cada hiperarista de la lista
            suc += c.states() # Concatenamos todos los estados destinos del hiperarista a la lista de sucesores
        return list(set(suc)) # Devolvemos la lista de sucesores con la previa eliminación de elementos repetidos

    """ Método para obtener un conjunto de predecesores de un estado en el hipergrafo"""
    def get_predecessors(self, s, table):
        pred = set()
        row = self.dict_state[s].row
        col = self.dict_state[s].col

        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if i >= 0 and i < len(table) and j >= 0 and j < len(table[0]) and not table[i][j].sink:
                    pred.add(table[i][j].id)

        return pred      

    """ método para reconstruir de best partial solution graph de forma recursiva """
    def get_bpsg_states(self, p, set_states, s):
        set_states.add(s) # Añadimos el estado a la lista
        best_action = p[s] # Obtenemos la mejor acción asociada al estado (empezando por el estado inicial)
        if best_action is not None: # Si hay una mejor acción asociada a ese estado
            for st in self.get_connector(s, best_action).states(): # Por cada estado sucesor de esa acción en el grafo
                if st not in set_states: # Si el estado no está en la lista
                    self.get_bpsg_states(p, set_states, st) # Llamamos de forma recursiva a la función para construir el árbol.
        return set_states # Devolvemos la lista de estados

    def get_bpsg_states_backwards(self, V, expanded, set_states, table, s):
        set_states.add(s)
        if s in expanded:
            predecessors = set(filter(lambda s: s not in set_states, self.get_predecessors(s, table)))
            if predecessors:
                bp = self.best_predecessor(predecessors, V)
                self.get_bpsg_states_backwards(V, expanded, set_states, table, bp)
        return set_states

    """ métodos para obtener el conjunto Z """
    def set_Z(self, graph, table, s, p, Z):
        predecessors = self.get_predecessors(s, table)
        for st in predecessors:
            if st in graph.states.keys() and st not in Z and not graph.dict_state[st].final:
                if s in self.get_connector(st, p[st]).states():
                    Z.add(st)
                    self.set_Z(graph, table, st, p, Z)
        return Z
    
    """método que dado un estado, devuelve el conector asociado a la acción dada"""
    def get_connector(self, state, action):
        con = None
        for c in self.states[state]:
            if c.action == action:
                con = c
                break
        return con

    def expand_forward(self, s, V, p, expanded, fringe, updated):
        updated.add(s)
        if s in expanded and p[s] is not None:
            for suc in self.get_connector(s, p[s]).states():
                if suc not in updated and not self.dict_state[suc].final:
                    fringe = self.expand_forward(suc, V, p, expanded, fringe, updated)
        elif s in fringe:
            expanded.add(s)
            fringe.remove(s)
            fringe = fringe | set(filter(lambda s: s not in expanded and not self.dict_state[s].final, self.get_successors(s)))            
        self.update_values([s], V, p)
        return fringe 
  
    """método busqueda hacia atrás rlao* """
    def expand_backward(self, s, V, p, table, expanded, fringe, s0, updated):
        updated.add(s)
        self.update_values([s], V, p)    
        if s in expanded and (p[s] is not None or self.dict_state[s].final):
            predecessors = set(filter(lambda s: s not in updated, self.get_predecessors(s, table)))
            for pred in predecessors:
                fringe = self.expand_backward(pred, V, p, table, expanded, fringe, s0, updated)
        elif s in fringe:
            expanded.add(s)
            fringe.remove(s)
            fringe = fringe | set(filter(lambda s: s not in expanded, self.get_predecessors(s, table)))
        return fringe

    """método búsqueda hacia atrás blao* """
    def expand_backward_(self, s, V, p, table, expanded, fringe, s0, updated):
        updated.add(s)
        self.update_values([s], V, p)    
        if s in expanded and (p[s] is not None or self.dict_state[s].final):
            predecessors = set(filter(lambda s: s not in updated, self.get_predecessors(s, table)))
            if predecessors:
                bp = self.best_predecessor(predecessors, V)
                fringe = self.expand_backward(bp, V, p, table, expanded, fringe, s0, updated)
        elif s in fringe:
            expanded.add(s)
            fringe.remove(s)
            fringe = fringe | set(filter(lambda s: s not in expanded, self.get_predecessors(s, table)))
        return fringe

    """método para actualizar los valores de los estados en la pila"""
    def update_values(self, stack, V, p):
        actions = {'NN', 'SS', 'EE', 'OO', 'NE', 'NO', 'SE', 'SO', '-'}
        best_action = None
        while stack:
            s = stack.pop()
            if not self.dict_state[s].final:
                minimum = float('inf')
                for a in actions:
                    c = self.get_connector(s, a)
                    if c is not None:
                        val = c.cost
                        for suc in c.states():
                            val += c.probs[suc] * V[suc]
                        if val < minimum:
                            minimum = val
                            best_action = a
                V[s] = minimum
                p[s] = best_action

    @staticmethod
    def best_predecessor(predecessors, V):
        min_value = float('inf')
        for pred in predecessors:
            if V[pred] < min_value:
                min_value = V[pred]
                best_pred = pred
        return best_pred