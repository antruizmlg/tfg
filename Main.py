from Problema import *
from LAO import *
import time

probabilidades_transicion = [[0.8, 0.2, 0, 0], # MOVERSE ARRIBA
                             [0.2, 0.8, 0, 0], # MOVERSE A LA DERECHA
                             [0, 0, 0.8, 0.2], # MOVERSE A LA IZQUIERDA
                             [0, 0.2, 0, 0.8]] # MOVERSE ABAJO

numFilas = 100
numCol = 100
numSumideros = 0

p = Problema(numFilas, numCol, numSumideros, probabilidades_transicion)
estado_por_id, hg, s0, h, pi = p.generar_problema()

p.print_info()

t_i = time.time()

VI_algorithm = VI(pi, h, estado_por_id)
VI_algorithm.run(hg)

t_f = time.time()

print("RESULTADO: ")
p.print_tablero(pi)

print("Tiempo usado: " + str(t_f - t_i))