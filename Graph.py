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
        return suc # Devolvemos la lista de sucesores con la previa eliminación de elementos repetidos

    """ Método para obtener un conjunto de predecesores de un estado en el hipergrafo"""
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


    """ métodos para acutalizar el conjunto de estados 'fringe' """
    def update_fringe_set(self, F, I, s):
        for st in self.get_successors(s): # Por cada sucesor de s en el hipergrafo
            if st not in I: # Si el sucesor no se encuentra en el conjunto I
                F.add(st) # Lo introducimos en el conjunto F

    def update_fringe_rlao(self, table, states, expanded):
        F = set()
        for state in states:
            predecessors = self.get_predecessors(state, table)
            for p in predecessors:
                if p not in expanded:
                    F.add(p)
        return F

    """ método para obtener estado no terminal """
    def get_no_final_state(self, states):
        for s in states: # Por cada estado en el conjunto states
            if not self.dict_state[s].final: # Si el estado no es terminal
                return s # Lo devolvemos
        return None # Si no hemos encontrado ningún estado no terminal en el conjunto, devolvemos None
    
    """método que dado un estado, devuelve el conector asociado a la acción dada"""
    def get_connector(self, state, action):
        con = None
        for c in self.states[state]:
            if c.action == action:
                con = c
                break
        return con

    """método para actualizar los valores de los estados en la pila"""
    def update_values(self, stack, V, p):
        actions = {'N', 'S', 'E', 'O'}
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
                
    def depth_first_search(self, envelope, i, fringe, interior, p, stack):
        if i in fringe: # Si el estado i no hay sido aún expandido
            stack.append(i)
            interior.add(i) # Lo añadimos al conjunto de estados interiores
            fringe.remove(i) # Lo eliminamos del conjunto de estados "fringe"
            fringe = fringe | set(filter(lambda s:not envelope.dict_state[s].final and s not in interior, self.get_successors(i)))
            # Actualizamos el conjunto fringe con los sucesores del estado i
            envelope.states[i] = self.states[i]
            # Expandimos el estado i en el grafo "envelope"
        elif i in interior: # Si el estado ha sido expandido
            stack.append(i)
            for suc in self.get_connector(i, p[i]).states(): # Para cada sucesor "greedy" del estado
                if suc not in stack and not self.dict_state[suc].final and not suc == i: # Si el sucesor no se encuentra ya en la pila y no es un estado
                    # final y no es el propio estado
                    fringe = self.depth_first_search(envelope, suc, fringe, interior, p, stack)
                    # Realizamos la llamada recursiva sobre el estado sucesor
        return fringe

    def backward_search(self, envelope, i, fringe, interior, V, s0, table, visited, stack):
        if i in fringe: # Si el estado i no hay sido aún expandido
            stack.append(i) # Añadimos el estado a la pila
            interior.add(i) # Lo añadimos al conjunto de estados interiores
            fringe.remove(i) # Lo eliminamos del conjunto de estados "fringe"
            fringe = fringe | set(filter(lambda s:not s == s0 and s not in interior, self.get_predecessors(i, table)))
            # Actualizamos el conjunto fringe con los sucesores del estado i
            envelope.states[i] = self.states[i]
            # Expandimos el estado i en el grafo "envelope"
        elif i in interior: # Si el estado ha sido expandido
            stack.append(i)  # Añadimos el estado a la pila
            predecessors = set(filter(lambda s: not s == i and s not in stack and not s == s0 and not s in visited, self.get_predecessors(i, table)))
            # Obtenemos todos los predecesores que no sean el mismo estado, no estén ya en la pila, no sean el estado inicial y no hayan sido visitados.
            if predecessors: # Si hay predecesores
                bp = self.best_predecessors(predecessors, V) # Obtenemos el mejor predecesor "greedy"
                fringe = self.backward_search(envelope, bp, fringe, interior, V, s0, table, visited, stack) # Llamada recursiva sobre predecesor "greedy"
        return fringe

    @staticmethod
    def best_predecessors(predecessors, V):
        min_value = float('inf')
        for pred in predecessors:
            if V[pred] < min_value:
                min_value = V[pred]
                best_pred = pred
        return best_pred