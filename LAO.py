from Hipergrafo import *
from PI import *
from VI import *
from copy import *
import time

class LAO:
    def __init__(self, est_id, hg, ini_state, h, pi, p, algorithm):
        self.ep_id = est_id
        self.hg = hg
        self.s0 = ini_state.id
        self.V = h
        self.p = pi
        self.problem = p
        self.algorithm = algorithm

    def LAO(self):
        F = [self.s0]
        I = []

        envelope_graph = Hipergrafo({self.s0: []})
        bpsg = deepcopy(envelope_graph)

        if self.algorithm == 'PI':
            algorithm = PI(self.p, self.V) 
        else:
            algorithm = VI(self.p, self.V)

        total_time = 0
        s = self.no_terminal_state(list(set(bpsg.estados) & set(F)))
        while s is not None:
            F = self.update_fringe_set(F, I, s) # Actualizamos el conjunto F
            I.append(s) # Introducimos s en el conjunto I
            envelope_graph = self.update_envelope_graph(envelope_graph, I, s)
            Z = Hipergrafo(self.get_z(bpsg, envelope_graph, s, {s:envelope_graph.estados[s]})) # Construimos el hipergrafo Z
            t_i = time.time()
            algorithm.run(Z)
            t_f = time.time()
            total_time += t_f - t_i
            bpsg = self.rebuild(envelope_graph, bpsg)
            s = self.no_terminal_state(list(set(bpsg.estados) & set(F)))
        print("VI time: "+str(total_time))
        return self.p, self.V

    def update_fringe_set(self, F, I, s):
        for st in self.hg.sucesores(s): # Por cada sucesor de s en el hipergrafo
            if st not in I: # Si el sucesor no se encuentra en el conjunto I
                F.append(st) # Lo introducimos en el conjunto F
        F = list(dict.fromkeys(F)) # Eliminamos los elementos repetidos
        F.remove(s) # Eliminamos el estado s
        return F

    def rebuild(self, envelope_graph, bpsg):
        bpsg_states = {} # Inicializamos el diccionario de estados a vacío
        for s in bpsg.estados.keys(): # Para cada estado del grafo solución
            if self.p.get_politica(s) is not None:
                for ha in envelope_graph.estados[s]: # Para cada hiperarista (asociado a una acción) del estado
                    if ha.accion == self.p.politica[s]: # Si la acción asociada a la hiperarista es la mejor acción según la política greedy actual
                        bpsg_states[s] = [ha] # Añadimos al diccionario una asociación con el estado y el hiperarista que refiere a su mejor acción según la política greedy
                        for st in ha.destino.keys():
                            if st not in bpsg_states.keys():
                                bpsg_states[st] = []
                        break
        return Hipergrafo(bpsg_states)

    def get_z(self, bpsg, envelope_graph, s, estados):
        for st in bpsg.estados.keys():
            if not st in estados.keys():
                for ha in bpsg.estados[st]:
                    if s in ha.destino.keys():
                        estados[st] = envelope_graph.estados[st]
                        if not s == st:
                            estados = self.get_z(bpsg, envelope_graph, st, estados)
        return estados

    def no_terminal_state(self, l):
        for e in l:
            if not self.ep_id[e].terminal:
                return e
        return None
    
    def update_envelope_graph(self, envelope_graph, I, s):
        envelope_graph.estados[s] = self.hg.estados[s]
        return envelope_graph