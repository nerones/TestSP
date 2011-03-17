#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    main_test_vns.py 0.0.10 
    las diferentes variaciones de VNS estan en algoritmos
"""
import os

from src.libs.mis_decoradores import captura_stdout
from src.libs.mis_decoradores import tiempo_ejecucion_
from src.load import tsp_load, tsp_sol_load
from src.tsp import *
from src.algoritmos import *


def menu():
    loop = True
    while loop:
        os.system('clear')
        print"""
    =====================================================
                    TSP Tester - version 0.0.1
    =====================================================

    1 - Cargar un Problema de TSPlib
    2 - Cargar un Problema de TSP en otro dir
    0 - Salir

    """
        opcion = raw_input('Elija una opcion y precione Enter: ')
        if opcion in ('0','1','2'):
            loop = False
        else:
            raw_input('Opcion No Valida...')
    return opcion

        
def main():
    #opc = menu()
    #if opc != '0':
        #file_name = raw_input('Nombre del fichero: ')
        #name, comment, vertex_list = tsp_load('ch130.tsp', False, True)
        name, comment, vertex_list = tsp_load('rat575.tsp', False, True)
        print 'Problema:', name
        print 'Comentarios:', comment
        dist_matrix = gen_distance_matrix(vertex_list)
        a = nearest_vertex(dist_matrix,len(vertex_list))
        solution_validator(a,len(vertex_list))
        value_a = get_obj_function_value(a, dist_matrix)
        
        for i in range(1):
            vns_opt_improved(a,value_a,20,30,0.98,dist_matrix)
        for i in range(1):
            vns_opt(a,value_a,20,30,dist_matrix)
        
        #memory = create_memory(10)
        #for i in range(len(memory)):
            #print memory[i]
        #a = [0,1,2,3,4,5,6,7,8,9]
        #x = a[:]
        #b = [1,3,2,4,0,5,6,7,8,9]
        #c = [1,3,2,4,0]
        #print len(a)
        #max = 1
        #for i in xrange(1000):
            #random.shuffle(a)
            #d,max = update_memory(memory,a,max)
        #for i in xrange(1000):
            #d,max = update_memory(memory,a,max)
        #ag,max = update_memory(memory,b,max)
        #for i in range(len(memory)):
            #print memory[i]
        #print max
        #print x
        #tr = create_neighbor(x,6,memory,max,0.95,memory)
        #print tr
        

if __name__ == '__main__':
    main()




