from Problem import *
from LAO import *
from RLAO import *
from BLAO import *
from ILAO import *
import time

import matplotlib
import matplotlib.pyplot as plt

"""Tres posibles sistemas de transiciones"""
probs_1 = {}
probs_2 = {}
probs_3 = {}
probs_4 = {}

"""Sistema 1"""
probs_1['N'] = {'N': 0.8, 'E': 0.1, 'O': 0.1}
probs_1['S'] = {'S': 0.8, 'E': 0.1, 'O': 0.1}
probs_1['E'] = {'E': 0.8, 'N': 0.1, 'S': 0.1}
probs_1['O'] = {'O': 0.8, 'N': 0.1, 'S': 0.1}

"""Sistema 2"""
probs_2['N'] = {'N': 0.8, 'E': 0.2}
probs_2['S'] = {'S': 0.8, 'O': 0.2}
probs_2['E'] = {'E': 0.8, 'S': 0.2}
probs_2['O'] = {'O': 0.8, 'N': 0.2}

"""Sistema 3"""
probs_3['N'] = {'N': 0.8, '-': 0.2}
probs_3['S'] = {'S': 0.8, '-': 0.2}
probs_3['E'] = {'E': 0.8, '-': 0.2}
probs_3['O'] = {'O': 0.8, '-': 0.2}

"""Número de filas, número de columnas y de sumideros""" 
rows = 30
columns = 30
sinks = 0

def solve_problem(problem, algorithm, heuristic = None):
    hg, s0, fs = problem.generate_problem() # Generamos el problema y obtenemos diccionario (estado id -> objeto estado), el hipergrafo
    # que representa el problema, el estado inicial, el heurístico y la política inicial

    p, h = problem.get_initial_policy_and_heuristic(heuristic)

    problem.print_info() # Imprimimos información del problema

    t_i = time.time() # Iniciamos contador

    # Ejecutamos algoritmo seleccionado por parámetros
    if algorithm == 'LAO*':
        lao_algorithm = LAO(hg, s0, h, p, problem.table, 'VI')
        lao_algorithm.LAO()
    elif algorithm == 'RLAO*':
        rlao_algorithm = RLAO(hg, fs, h, p, problem.table, 'VI')
        rlao_algorithm.RLAO()
    elif algorithm == 'ILAO*':
        ilao_algorithm = ILAO(hg, s0, h, p, problem.table, 'VI')
        ilao_algorithm.ILAO()        
    elif algorithm == 'BLAO*':
        blao_algorithm = BLAO(hg, s0, fs, h, p, problem.table, 'VI')
        blao_algorithm.BLAO()
    elif algorithm == 'VI':
        vi_algorithm = Value_Iteration(hg, p, h)
        vi_algorithm.run(hg.states.keys())
    elif algorithm == 'PI':
        pi_algorithm = Policy_Iteration(hg, p, h)
        pi_algorithm.run(hg.states.keys())

    # Finalizamos contador
    t_f = time.time()

    #Imprimimos resultado
    print("RESULTADO: ")
    problem.print_solution(p)

    # Imprimimos tiempo usado
    print("Tiempo usado (" + algorithm + "): " + str(t_f - t_i))

p_1 = Problem(rows, columns, sinks, probs_2) # Creamos la instancia del problema, con el número de filas, columnas, sumideros 
                                                        # y el sistema transitorio
solve_problem(p_1, 'ILAO*') # Ejecutamos el algoritmo sobre elegido sobre el problema instanciado