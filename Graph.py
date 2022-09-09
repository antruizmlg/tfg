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
        sol = set()
        x = self.dict_state[s].x
        y = self.dict_state[s].y
        w = self.dict_state[s].w
        z = self.dict_state[s].z

        x_pt = self.possible_transitions(x, len(table))
        y_pt = self.possible_transitions(y, len(table[0]))
        w_pt = self.possible_transitions(w, len(table[0][0]))
        z_pt = self.possible_transitions(z, len(table[0][0][0]))

        for i in x_pt:
            state = table[i][y][w][z]
            if not state.sink:
                sol.add(state.id)
        for i in y_pt:
            state = table[x][i][w][z]
            if not state.sink:
                sol.add(state.id)
        for i in w_pt:
            state = table[x][y][i][z]
            if not state.sink:
                sol.add(state.id)
        for i in z_pt:
            state = table[x][y][w][i]
            if not state.sink:
                sol.add(state.id)
        return sol

    @staticmethod
    def possible_transitions(val, total_dim):
        pt = []
        if val - 1 >= 0:
            pt.append(val - 1)
        if val + 1 < total_dim:
            pt.append(val + 1)
        return pt

    """ método para reconstruir de best partial solution graph de forma recursiva """
    def get_bpsg_states(self, p, set_states, s):
        set_states.add(s) # Añadimos el estado a la lista
        best_action = p[s] # Obtenemos la mejor acción asociada al estado (empezando por el estado inicial)
        if best_action is not None: # Si hay una mejor acción asociada a ese estado
            for st in self.get_connector(s, best_action).states(): # Por cada estado sucesor de esa acción en el grafo
                if st not in set_states: # Si el estado no está en la lista
                    self.get_bpsg_states(p, set_states, st) # Llamamos de forma recursiva a la función para construir el árbol.
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


    """ métodos para acutalizar el conjunto de estados 'fringe' """
    def update_fringe_set(self, F, I, s):
        for st in self.get_successors(s): # Por cada sucesor de s en el hipergrafo
            if st not in I and not self.dict_state[st].final: # Si el sucesor no se encuentra en el conjunto I
                F.add(st) # Lo introducimos en el conjunto F
    
    """método que dado un estado, devuelve el conector asociado a la acción dada"""
    def get_connector(self, state, action):
        con = None
        for c in self.states[state]:
            if c.action == action:
                con = c
                break
        return con

    def expand_forward(self, s, V, p, expanded):
        expanded.add(s)
        action = p[s]
        if action is not None:
            for suc in self.get_connector(s, action).states():
                if suc not in expanded:
                    self.expand_forward(suc, V, p, expanded)
        self.update_values([s], V, p)    
  
    def expand_backward(self, s, V, p, table, expanded):
        expanded.add(s)
        interior = p[s] is not None
        self.update_values([s], V, p)
        if interior or self.dict_state[s].final:
            predecessors = set(filter(lambda s: s not in expanded, self.get_predecessors(s, table)))
            for pred in predecessors:
                self.expand_backward(pred, V, p, table, expanded)

    """método para actualizar los valores de los estados en la pila"""
    def update_values(self, stack, V, p):
        actions = {'1', '2', '3', '4', '5', '6', '7', '8'}
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
                V[s] = round(minimum, 2)
                if best_action is None:
                    print("")
                p[s] = best_action

    @staticmethod
    def best_predecessor(predecessors, V):
        min_value = float('inf')
        for pred in predecessors:
            if V[pred] < min_value:
                min_value = V[pred]
                best_pred = pred
        return best_pred