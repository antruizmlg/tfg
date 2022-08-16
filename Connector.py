""" clase que contiene la acción asociada al conector, 
    el coste asociado al conector y un diccionario con
    asociaciones (estado -> probabilidad)"""
class Connector:
    def __init__(self, probs, action, cost):
        self.probs = probs
        self.action = action
        self.cost = cost

    def states(self):
        return self.probs.keys()