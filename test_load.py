#!/usr/bin/python

"""
    Prueba de carga un fichero tsp
"""

import sys

from src.load import tsp_load, tsp_sol_load
from src.tsp import * #gen_distance_matrix, distance, get_obj_function_value
from src.algoritmos import * #opt2, opt2_, opt3, opt3_, vns_opt2


def main():
    #f_name ,s_exa = tsp_sol_load('pr76.opt.tour', False, True)
    name, comment, vertex_list = tsp_load('p654.tsp', False, True)

    print 'Problema:', name
    print 'Comentarios:', comment
    m = gen_distance_matrix(vertex_list)

    #s1 = gen_random_sol(vertex_list)
    #print 'rand', get_obj_function_value(s1, m)

    #anda para el ojete
    #t = type_moon(vertex_list, m)
    #print 'type_moon', get_obj_function_value(t, m)

    s0 = greedy(vertex_list, m, 502)
    l = len(s0)
    print 'greedy', get_obj_function_value(s0, m)

    s1 = vns_opt2(s0, m)
    print 'vns', get_obj_function_value(s1, m)
    if l != len(s1):
        print 'mankeada'

    s2 = opt3_(s1, m)
    print 'opt3', get_obj_function_value(s2, m)
    if l != len(s2):
        print 'mankeada'

if __name__ == '__main__':
    main()
