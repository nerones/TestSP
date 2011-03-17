#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.load import tsp_load, tsp_sol_load
from src.tsp import *
from src.extras import *

def main():
    name, comment, vertex_list = tsp_load('p654.tsp', False, True)
    dist_matrix = gen_distance_matrix(vertex_list)

    #mejor valor encontrado, sacado de la tabla
    optimo = 34643

    #fichero con la solucion a cargar
    soluc_a = load_solucion('mejor_sol_p654_1.dat')
    value_a = get_obj_function_value(soluc_a, dist_matrix)
    percent = (value_a - optimo) * 100 / optimo

    print '\n----- Resultados -----'
    print 'Optimo Tabla: ', optimo
    print 'Mi Optimo', value_a
    print 'Porcentaje de Error', percent

main()
