""" clase que contiene la acción asociada al conector, 
    el coste asociado al conector y un diccionario con
    asociaciones (estado -> probabilidad)"""
class Hiperarista:
    def __init__(self, dest, accion, coste):
        self.destino = dest
        self.accion = accion
        self.coste = coste