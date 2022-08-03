from Hipergrafo import *
from PI import *
from VI import *
from copy import *
import time

class LAO:
    def __init__(self, dict_state, hg, ini_state, h, pi, p, algorithm):
        self.dict_state = dict_state
        self.hg = hg
        self.s0 = ini_state.id
        self.V = h
        self.p = pi
        self.pr = p
        self.algorithm = algorithm

    def LAO(self):
        F = [self.s0]
        I = []

        eg_sizes = []
        sg_sizes = []
        Z_sizes = []

        envelope_graph = Hipergrafo({self.s0: []})
        bpsg = deepcopy(envelope_graph)

        if self.algorithm == 'PI':
            algorithm = PI(self.p, self.V, self.dict_state) 
        if self.algorithm == 'VI':
            algorithm = VI(self.p, self.V, self.dict_state)

        s = self.no_terminal_state(list(set(bpsg.estados) & set(F)))
        while s is not None:
            F = self.update_fringe_set(F, I, s) # Actualizamos el conjunto F
            I.append(s) # Introducimos s en el conjunto I
            envelope_graph = self.update_envelope_graph(envelope_graph, I, s)
            Z = Hipergrafo(self.get_z(envelope_graph, s, {s:envelope_graph.estados[s]})) # Construimos el hipergrafo Z 
            algorithm.run(Z)
            bpsg = Hipergrafo(self.rebuild(envelope_graph, {}, self.s0))
            s = self.no_terminal_state(list(set(bpsg.estados) & set(F)))
            eg_sizes.append(len(envelope_graph.estados))
            sg_sizes.append(len(bpsg.estados))
            Z_sizes.append(len(Z.estados))
        return eg_sizes, sg_sizes, Z_sizes

    def update_fringe_set(self, F, I, s):
        for st in self.hg.sucesores(s): # Por cada sucesor de s en el hipergrafo
            if st not in I: # Si el sucesor no se encuentra en el conjunto I
                F.append(st) # Lo introducimos en el conjunto F
        F = list(dict.fromkeys(F)) # Eliminamos los elementos repetidos
        F.remove(s) # Eliminamos el estado s
        return F

    def rebuild(self, envelope_graph, dict, s):
        best_action = self.p.get_politica(s)
        if best_action is not None:
            for ha in envelope_graph.estados[s]:
                if ha.accion == best_action and s not in dict.keys():
                    dict[s] = [ha]
                    for st in ha.destino.keys():
                        dict = self.rebuild(envelope_graph, dict, st)
        elif s not in dict.keys():
                dict[s] = []
        return dict

    def get_z(self, envelope_graph, s, estados):
        for st in envelope_graph.estados.keys():
            if not st in estados.keys():
                for ha in envelope_graph.estados[st]:
                    if s in ha.destino.keys() and ha.accion == self.p.get_politica(st):
                        estados[st] = envelope_graph.estados[st]
                        if not s == st:
                            estados = self.get_z(envelope_graph, st, estados)
                        break
        return estados

    def no_terminal_state(self, l):
        for e in l:
            if not self.dict_state[e].terminal:
                return e
        return None
    
    def update_envelope_graph(self, envelope_graph, I, s):
        envelope_graph.estados[s] = self.hg.estados[s]
        return envelope_graph