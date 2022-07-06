class PI:
    def __init__(self, hipergrafo, politica, V):
        self.hipergrafo = hipergrafo
        self.politica = politica
        self.V = V
    
    def policy_iterations(self):
        while True:
            old_policy = self.politica.copy() # Hacemos una copia de la política actual

            self.policy_evaluation() # Modificamos la función de valor mediante evaluación de la política

            # self.policy_improvement() # Obtenemos la mejor política con la nueva función de valor

            if all(old_policy.politicas[s] == self.politica.politicas[s] for s in old_policy.estados): # Si la nueva política coincide con la anterior, hemos llegado a una convergencia.
                break

    def policy_evaluation(self):
        while True:
            oldV = self.V # Almacenamos la antigua función de valor

            for ha in self.hipergrafo.hiperaristas: # Para cada hiperarista del hipergrafo.
                if self.politica.getPolitica(ha.source) == ha.accion: # Si la acción asociada al hiperarista coincide con la que dicta la política para ese estado
                    sum = 0
                    for estado in ha.destino.keys(): # Para cada estado destino
                        sum += ha.destino[estado] * oldV.getValor(estado) # Sumamos la probabilidad de alcanzar ese estado desde el actual por el valor de ese estado
                    self.V.setValor(estado, ha.coste + sum) # Modificamos el nuevo valor del estado actual.

            if all(list(oldV.values())[s] == list(self.V.values())[s] for s in oldV.keys()):
                break

    def policy_improvement(self):
        estados = list(self.politica.keys()) # Inicializamos una lista con todos los estados
        minimo_coste_actual = [999999 for e in estados] # Inicializamos una lista que almacenará el menor coste encontrado para cada estado en un momento determinado
        mejor_accion_actual = [list(self.politica.values())[0] for e in estados]  # Inicializamos una lista que almacenará la mejor política encontrada para cada estado en un momento determinado

        for ha in self.hipergrafo.hiperaristas: # Para cada arista en el conjunto de aristas del grafo.
            i = estados.index(ha.source) # Obtenemos el índice en la lista de estados
            sum = 0 
            for e in ha.destino.keys():
                sum += ha.destino[e] * self.V.getValor(e)
            valor_ha = ha.coste + sum # Calculamos el valor de realizar la acción de la hiperarista desde ese estado.
            if valor_ha < minimo_coste_actual[i]: # Si ese valor (coste) es menor que el menor encontrado hasta el momento
                minimo_coste_actual[i] = valor_ha # Actualizamos el menor valor
                mejor_accion_actual[i] = ha.accion # Actualizamos la mejor política

        for ind in range(len(estados)): # Recorremos la lista de estado.
            self.politica[estados[ind]] = mejor_accion_actual[i]  # Actualizamos la política: para cada estado, almacenamos su mejor acción en el diccionario.