from Problema import *
from LAO import *
import time

probabilidades_transicion = {}

probabilidades_transicion['N'] = {'N': 0.8, 'E': 0.1, 'O': 0.1}
probabilidades_transicion['S'] = {'S': 0.8, 'E': 0.1, 'O': 0.1}
probabilidades_transicion['E'] = {'E': 0.8, 'N': 0.1, 'S': 0.1}
probabilidades_transicion['O'] = {'O': 0.8, 'N': 0.1, 'S': 0.1}
 
numFilas = 10
numCol = 10
numSumideros = 0

p = Problema(numFilas, numCol, numSumideros, probabilidades_transicion)
dict_state, hg, s0, h, pi = p.generar_problema()

p.print_info()

t_i = time.time()

lao_algorithm = LAO(dict_state, hg, s0, h, pi, p, 'VI')
lao_algorithm.LAO()

t_f = time.time()

print("RESULTADO: ")
p.print_solution(pi)

print("Tiempo usado (LAO*): " + str(t_f - t_i))

estado_por_id, hg, s0, h, pi = p.generar_problema()

t_i = time.time()

algorithm = VI(pi, h, estado_por_id)
algorithm.run(hg)

t_f = time.time()
print("Tiempo usado (VI): " + str(t_f - t_i))

p.print_solution(pi)