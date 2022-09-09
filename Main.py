from Problem import *
from LAO import *
from RLAO import *
from BLAO import *
from ILAO import *
import time

"""Tres posibles sistemas de transiciones"""
probs_1 = {}

"""Sistema 3"""
probs_1['1'] = {'1': 0.8, '-': 0.2}
probs_1['2'] = {'2': 0.8, '-': 0.2}
probs_1['3'] = {'3': 0.8, '-': 0.2}
probs_1['4'] = {'4': 0.8, '-': 0.2}
probs_1['5'] = {'5': 0.8, '-': 0.2}
probs_1['6'] = {'6': 0.8, '-': 0.2}
probs_1['7'] = {'7': 0.8, '-': 0.2}
probs_1['8'] = {'8': 0.8, '-': 0.2}
probs_1['9'] = {'9': 0.8, '-': 0.2}
probs_1['10'] = {'10': 0.8, '-': 0.2}
probs_1['11'] = {'11': 0.8, '-': 0.2}
probs_1['12'] = {'12': 0.8, '-': 0.2}
probs_1['13'] = {'13': 0.8, '-': 0.2}
probs_1['14'] = {'14': 0.8, '-': 0.2}
probs_1['15'] = {'15': 0.8, '-': 0.2}


"""Número de filas, número de columnas y de sumideros""" 
x = 10
y = 10
w = 10
z = 10
sinks = 0

def solve_problem(problem, algorithm):
    hg, s0, fs = problem.generate_problem() # Generamos el problema y obtenemos diccionario (estado id -> objeto estado), el hipergrafo
    # que representa el problema, el estado inicial, el heurístico y la política inicial

    p, h = problem.get_initial_policy_and_heuristic()
    problem.print_info() # Imprimimos información del problema

    t_i = time.time() # Iniciamos contador
    # Ejecutamos algoritmo seleccionado por parámetros
    if algorithm == 'LAO*':
        lao_algorithm = LAO(hg, s0, h, p, problem)
        lao_algorithm.LAO()
    elif algorithm == 'RLAO*':
        rlao_algorithm = RLAO(hg, s0, fs, h, p, problem)
        rlao_algorithm.RLAO()
    elif algorithm == 'ILAO*':
        ilao_algorithm = ILAO(hg, s0, h, p, problem)
        ilao_algorithm.ILAO()        
    elif algorithm == 'BLAO*':
        blao_algorithm = BLAO(hg, s0, fs, h, p, problem)
        blao_algorithm.BLAO()
    elif algorithm == 'VI':
        vi_algorithm = Value_Iteration(hg, p, h, gamma = 0.99)
        vi_algorithm.run(hg.states.keys())

    # Finalizamos contador
    t_f = time.time()

    # Imprimimos tiempo usado
    print("Tiempo usado (" + algorithm + "): " + str(t_f - t_i))

p_1 = Problem(x, y, w, z, sinks, probs_1) # Creamos la instancia del problema, con el número de filas, columnas, sumideros 
                                                            # y el sistema transitorio
solve_problem(p_1, 'VI') # Ejecutamos el algoritmo sobre elegido sobre el problema instanciado
                                                        # y el sistema transitorio