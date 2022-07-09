from EstadoTest import *
from Hiperarista import *
from Hipergrafo import *
from LAO import *
from FuncionDeValor import *
from Politica import *

s1 = EstadoTest('s1')
s2 = EstadoTest('s2')
s3 = EstadoTest('s3')
s4 = EstadoTest('s4')
s5 = EstadoTest('s5')
s6 = EstadoTest('s6')
s7 = EstadoTest('s7')
s8 = EstadoTest('s8')

h1_1 = Hiperarista(s1, {'s2':0.8, 's1':0.2}, 'ARRIBA', 0.6)
h1_2 = Hiperarista(s1, {'s1':0.8, 's2':0.1, 's8': 0.1}, 'IZQUIERDA', 0.4)
h1_3 = Hiperarista(s1, {'s1':0.8, 's2':0.1, 's8': 0.1}, 'DERECHA', 0.4)
h1_4 = Hiperarista(s1, {'s8':0.8, 's1':0.2}, 'ABAJO', 0.2)

h2_1 = Hiperarista(s2, {'s2':0.9, 's3':0.1}, 'ARRIBA', 0.6)
h2_2 = Hiperarista(s2, {'s2':0.9, 's1':0.1}, 'IZQUIERDA', 0.4)
h2_3 = Hiperarista(s2, {'s3':0.8, 's2':0.1, 's1':0.1}, 'DERECHA', 0.4)
h2_4 = Hiperarista(s2, {'s1':0.8, 's2':0.1, 's3':0.1}, 'ABAJO', 0.2)

h3_1 = Hiperarista(s3, {'s3':0.8, 's2':0.1, 's4':0.1}, 'ARRIBA', 0.6)
h3_2 = Hiperarista(s3, {'s2':0.8, 's3':0.2}, 'IZQUIERDA', 0.4)
h3_3 = Hiperarista(s3, {'s4':0.8, 's3':0.2}, 'DERECHA', 0.4)
h3_4 = Hiperarista(s3, {'s3':0.8, 's2':0.1, 's4':0.1}, 'ABAJO', 0.2)

h4_1 = Hiperarista(s4, {}, 'ARRIBA', 0)
h4_2 = Hiperarista(s4, {}, 'IZQUIERDA', 0)
h4_3 = Hiperarista(s4, {}, 'DERECHA', 0)
h4_4 = Hiperarista(s4, {}, 'ABAJO', 0)

h5_1 = Hiperarista(s5, {'s4':0.8, 's5':0.2}, 'ARRIBA', 0.6)
h5_2 = Hiperarista(s5, {'s5':0.8, 's4':0.1, 's6':0.1}, 'IZQUIERDA', 0.4)
h5_3 = Hiperarista(s5, {'s5':0.8, 's4':0.1, 's6':0.1}, 'DERECHA', 0.4)
h5_4 = Hiperarista(s5, {'s6':0.8, 's5':0.2}, 'ABAJO', 0.2)

h6_1 = Hiperarista(s6, {'s5':0.8, 's6':0.1, 's7':0.1}, 'ARRIBA', 0.6)
h6_2 = Hiperarista(s6, {'s7':0.8, 's5':0.1, 's6':0.1}, 'IZQUIERDA', 0.4)
h6_3 = Hiperarista(s6, {'s6':0.9, 's5':0.1}, 'DERECHA', 0.4)
h6_4 = Hiperarista(s6, {'s6':0.9, 's7':0.1}, 'ABAJO', 0.2)

h7_1 = Hiperarista(s7, {'s7':0.8, 's6':0.1, 's8':0.1}, 'ARRIBA', 0.6)
h7_2 = Hiperarista(s7, {'s8':0.8, 's7':0.2}, 'IZQUIERDA', 0.4)
h7_3 = Hiperarista(s7, {'s6':0.8, 's7':0.2}, 'DERECHA', 0.4)
h7_4 = Hiperarista(s7, {'s7':0.8, 's6':0.1, 's8':0.1}, 'ABAJO', 0.2)

h8_1 = Hiperarista(s8, {'s1':0.8, 's7':0.1, 's8':0.1}, 'ARRIBA', 0.6)
h8_2 = Hiperarista(s8, {'s8':0.9, 's1':0.1}, 'IZQUIERDA', 0.4)
h8_3 = Hiperarista(s8, {'s7':0.8, 's1':0.1, 's8':0.1}, 'DERECHA', 0.4)
h8_4 = Hiperarista(s8, {'s8':0.9, 's7':0.1}, 'ABAJO', 0.2)

hg = Hipergrafo({'s1': s1, 's2': s2, 's3': s3, 's4': s4, 's5': s5, 's6': s6, 's7': s7, 's8': s8}, [h1_1, h1_2, h1_3, h1_4, h2_1, h2_2, h2_3, h2_4, h3_1, h3_2, h3_3, h3_4, 
        h4_1, h4_2, h4_3, h4_4, h5_1, h5_2, h5_3, h5_4, h6_1, h6_2, h6_3, h6_4, h7_1, h7_2, h7_3, h7_4, h8_1, h8_2, h8_3, h8_4])

heuristico = FuncionDeValor({'s1': 3, 's2': 2, 's3': 1, 's4': 0, 's5': 1, 's6': 2, 's7': 3, 's8': 4})

#La política inicial es arbitraria
politicaInicial = Politica({'s1': 'ABAJO', 's2': 'ABAJO', 's3': 'ABAJO', 's4': 'ARRIBA', 's5': 'DERECHA', 's6': 'IZQUIERDA', 's7': 'IZQUIERDA', 's8': 'IZQUIERDA'})

lao_algorithm = LAO(hg, s1, heuristico, politicaInicial, 'PI')
politica, V = lao_algorithm.LAO()
print(politica.politica)