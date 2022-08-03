""" esta clase representa un diccionario con asociaciones (estado -> valor)"""
class FuncionDeValor:    
    def __init__(self, dictValores):
        self.dv = dictValores

    def set_valor(self, estado, nuevoValor):
        self.dv[estado] = nuevoValor

    def get_valor(self, estado):
        return self.dv[estado]