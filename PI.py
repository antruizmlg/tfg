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
                    self.V.setValor(ha.coste + sum) # Modificamos el nuevo valor del estado actual.

            if all(list(oldV.values())[s] == list(self.V.values())[s] for s in oldV.keys()):
                break