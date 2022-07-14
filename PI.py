from copy import *

class PI:
    def __init__(self, hg, p, V, ep_id):
        self.hg = hg
        self.p = p
        self.V = V
        self.ep_id = ep_id
    
    def policy_iteration(self):
        while True:
            old_policy = deepcopy(self.p) # Hacemos una copia de la política actual

            self.policy_evaluation() # Modificamos la función de valor mediante evaluación de la política

            self.policy_improvement() # Obtenemos la mejor política con la nueva función de valor

            if all(old_policy.politica[s] == self.p.politica[s] for s in old_policy.politica.keys()): # Si la nueva política coincide con la anterior, hemos llegado a una convergencia.
                break

    def policy_evaluation(self):
        while True:
            oldV = deepcopy(self.V) # Almacenamos la antigua función de valor

            for s in self.hg.estados.keys(): # Para cada estado
                if not self.ep_id[s].sumidero: # Si el estado no es un sumidero
                    for ha in self.hg.estados[s]: # Para cada hiperarista asociada a ese estado
                        if self.p.get_politica(s) == ha.accion: # Si la acción dictada por la política coincide con la asociada al hiperarista, esta es la acción que debemos evaluar
                            nv = ha.coste
                            for st in ha.destino.keys(): # Para cada estado destino
                                nv += ha.destino[st] * oldV.get_valor(st) # Sumamos la probabilidad de alcanzar ese estado desde el actual por el valor de ese estado
                            self.V.set_valor(s, round(nv, 2)) # Modificamos el nuevo valor del estado actual.
                            break

            if all(oldV.dv[s] == self.V.dv[s] for s in oldV.dv.keys()):
                break

    def policy_improvement(self):
        for s in self.hg.estados.keys(): # Para cada estado del grafo.
            min_coste = float('inf')
            for ha in self.hg.estados[s]: # Para cada hiperarista asociada a ese estado.
                coste_accion = ha.coste
                for e in ha.destino.keys(): # Para cada estado alcanzable mediante la acción
                    coste_accion += ha.destino[e] * self.V.get_valor(e) # Sumamos la probabilidad de alcanzar el estado por el valor del estado.
                if coste_accion < min_coste: # Si el coste de la acción es menor que el minimo encontrado hasta el momento
                    mejor_accion = ha.accion # Actualizamos la mejor acción hasta el momento
                    min_coste = coste_accion # Actualizamos el mínimo coste encontrado hasta el momento
            self.p.set_politica(s, mejor_accion) # Actualizamos la política con la mejor acción