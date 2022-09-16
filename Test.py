from Problem import *
from LAO import *
from RLAO import *
from BLAO import *
from ILAO import *
import time
import sys

"""Tres posibles sistemas de transiciones"""
probs_1 = {}
probs_2 = {}
probs_3 = {}

"""Sistema 1"""
probs_1['NN'] = {'NN': 0.8, 'NE': 0.1, 'NO': 0.1}
probs_1['SS'] = {'SS': 0.8, 'SE': 0.1, 'SO': 0.1}
probs_1['EE'] = {'EE': 0.8, 'NE': 0.1, 'SE': 0.1}
probs_1['OO'] = {'OO': 0.8, 'NO': 0.1, 'SO': 0.1}
probs_1['NE'] = {'NE': 0.8, 'EE': 0.1, 'NN': 0.1}
probs_1['NO'] = {'NO': 0.8, 'NN': 0.1, 'OO': 0.1}
probs_1['SE'] = {'SE': 0.8, 'SS': 0.1, 'EE': 0.1}
probs_1['SO'] = {'SO': 0.8, 'OO': 0.1, 'SS': 0.1}
probs_1['--'] = {'--': 1}

"""Sistema 2"""
probs_2['NN'] = {'NN': 0.9, 'NE': 0.1}
probs_2['SS'] = {'SS': 0.9, 'SO': 0.1}
probs_2['EE'] = {'EE': 0.9, 'SE': 0.1}
probs_2['OO'] = {'OO': 0.9, 'NO': 0.1}
probs_2['NE'] = {'NE': 0.9, 'EE': 0.1}
probs_2['NO'] = {'NO': 0.9, 'NN': 0.1}
probs_2['SE'] = {'SE': 0.9, 'SS': 0.1}
probs_2['SO'] = {'SO': 0.9, 'OO': 0.1}
probs_2['--'] = {'--': 1}

"""Sistema 3"""
probs_3['NN'] = {'NN': 0.9, '--': 0.1}
probs_3['SS'] = {'SS': 0.9, '--': 0.1}
probs_3['EE'] = {'EE': 0.9, '--': 0.1}
probs_3['OO'] = {'OO': 0.9, '--': 0.1}
probs_3['NE'] = {'NE': 0.9, '--': 0.1}
probs_3['SE'] = {'SE': 0.9, '--': 0.1}
probs_3['NO'] = {'NO': 0.9, '--': 0.1}
probs_3['SO'] = {'SO': 0.9, '--': 0.1}
probs_3['--'] = {'--': 1}

"""Número de filas, número de columnas y de sumideros""" 
rows = 50
columns = 50
sinks = 0

sys.setrecursionlimit(1000000)
def solve_problem(problem, algorithm):
    hg, s0, fs = problem.generate_problem() # Generamos el problema y obtenemos diccionario (estado id -> objeto estado), el hipergrafo
    # que representa el problema, el estado inicial, el heurístico y la política inicial

    p, h = problem.get_initial_policy_and_heuristic(algorithm)
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
        vi_algorithm = Value_Iteration(hg, p, h, gamma = 0.95)
        vi_algorithm.run(hg.states.keys())

    # Finalizamos contador
    t_f = time.time()

    #Imprimimos resultado
    print("RESULTADO: ")
    problem.print_solution(p)

    # Imprimimos tiempo usado
    print("Tiempo usado (" + algorithm + "): " + str(t_f - t_i))

p_1 = Problem(rows, columns, sinks, probs_2) # Creamos la instancia del problema, con el número de filas, columnas, sumideros 
                                                            # y el sistema transitorio
solve_problem(p_1, 'LAO*') # Ejecutamos el algoritmo sobre elegido sobre el problema instanciado
                                                        # y el sistema transitorio