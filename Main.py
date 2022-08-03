from Problema import *
from LAO import *
import time

probs_1 = {}
probs_2 = {}
probs_3 = {}

probs_1['N'] = {'N': 0.8, 'E': 0.1, 'O': 0.1}
probs_1['S'] = {'S': 0.8, 'E': 0.1, 'O': 0.1}
probs_1['E'] = {'E': 0.8, 'N': 0.1, 'S': 0.1}
probs_1['O'] = {'O': 0.8, 'N': 0.1, 'S': 0.1}

probs_2['N'] = {'N': 0.8, 'E': 0.2}
probs_2['S'] = {'S': 0.8, 'O': 0.2}
probs_2['E'] = {'E': 0.8, 'S': 0.2}
probs_2['O'] = {'O': 0.8, 'N': 0.2}

probs_3['N'] = {'N': 0.8, '-': 0.2}
probs_3['S'] = {'S': 0.8, '-': 0.2}
probs_3['E'] = {'E': 0.8, '-': 0.2}
probs_3['O'] = {'O': 0.8, '-': 0.2}
 
numFilas = 10
numCol = 10
numSumideros = 0

def run_algorithm(p, algorithm):
    dict_state, hg, s0, h, pi = p.generar_problema()

    p.print_info()

    t_i = time.time()

    lao_algorithm = LAO(dict_state, hg, s0, h, pi, p, algorithm)
    eg_sizes, sg_sizes, Z_sizes = lao_algorithm.LAO()

    t_f = time.time()

    print("RESULTADO: ")
    p.print_solution(pi)

    print("Tiempo usado: " + str(t_f - t_i))

p_1 = Problema(numFilas, numCol, numSumideros, probs_1)
run_algorithm(p_1, 'VI')