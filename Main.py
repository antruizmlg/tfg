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

probs = {'1': probs_1, '2': probs_2, '3': probs_3}

sys.setrecursionlimit(1000000)
def solve_problem(problem, algorithm, output):
    hg, s0, fs = problem.generate_problem() # Generamos el problema y obtenemos el hipergrafo que representa el problema, el estado inicial, el heurístico y la política inicial

    p, h = problem.get_initial_policy_and_heuristic(algorithm)
    problem.print_info() # Imprimimos información del problema

    t_i = time.time() # Iniciamos contador
    # Ejecutamos algoritmo seleccionado por parámetros
    if algorithm == 1:
        lao_algorithm = LAO(hg, s0, h, p, problem)
        lao_algorithm.LAO()
    elif algorithm == 2:
        rlao_algorithm = RLAO(hg, s0, fs, h, p, problem)
        rlao_algorithm.RLAO()
    elif algorithm == 3:
        ilao_algorithm = ILAO(hg, s0, h, p, problem)
        ilao_algorithm.ILAO()        
    elif algorithm == 4:
        blao_algorithm = BLAO(hg, s0, fs, h, p, problem)
        blao_algorithm.BLAO()
    elif algorithm == 5:
        vi_algorithm = Value_Iteration(hg, p, h, gamma = 0.95)
        vi_algorithm.run(hg.states.keys())

    # Finalizamos contador
    t_f = time.time()

    #Imprimimos resultado
    sol = problem.print_solution(p)
    print("RESULTADO: ")
    print(sol)

    # Imprimimos tiempo usado
    print("Tiempo usado: " + str(t_f - t_i))

    if output == 'S':
        f = open('res.txt', 'w')
        f.write(sol)
        f.close()

rows = int(input("Ingrese el número de filas: "))
cols = int(input("Ingrese el número de columnas: "))
while True:
    sinks = int(input("Ingrese el porcentaje (%) de sumideros: [0-100) "))
    if sinks >= 0 and sinks < 100:
        break

print("SI HAY SUMIDEROS SE RECOMIENDA USAR SISTEMA 3, YA QUE ES EL ÚNICO SISTEMA QUE ASEGURA LA EXISTENCIA DE SOLUCIÓN SI EL PORCENTAJE DE SUMIDEROS ES ALTO")
while True:
    system = input("Ingrese el sistema que quiera utilizar: (1-3) ")
    if system == '1' or system == '2' or system == '3':
        break

print("1 -> LAO*")
print("2 -> RLAO*")
print("3 -> ILAO*")
print("4 -> BLAO*")
print("5 -> VI")

while True:
    algorithm = int(input("¿Qué algoritmo desea utilizar? (1-5) "))
    if algorithm >= 1 and algorithm <= 5:
        break

while True:
    output = input("¿Desea volcar resultado en un fichero? (S/N) ")
    if output == 'S' or output == 'N':
        break

p = Problem(rows, cols, rows * cols * (sinks/100), probs[system])
solve_problem(p, algorithm, output)
