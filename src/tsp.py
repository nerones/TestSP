#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Version: 0.0.7 (Beta)

    Autor: Ricardo D. Quiroga->L2Radamanthys

    Fecha: 11 de Junio de 2010

    E-mail:
        l2radamanthys@gmail.com
        l2radamanthys@saltalug.org.ar
        ricardoquiroga.dev@gmail.com

    SitioWeb:
        http://www.l2radamanthys.com.ar
        http://l2radamanthys.blogspot.com

    Descripcion:
        Conjunto basico de funciones para trabajar con TSP, las mismas fueron
        escritas basandose en el original TSPMain.py que tambien se adjunta.

    Terminos y Condiciones:
        Este Script es Software Libre y esta bajo terminos de la GNU General
        Public Licence publicada por la Free Software Foundation
        (http://www.fsf.org) version 2 de la licencia u/o (opcionalmente)
        otras versiones de la licencia.

        Usted puede redistribuir y/o modificar este Script
        siguiendo los terminos de la GNU General Public Licence
        para mayor informacion vease la copia de la licencia que
        se adjunta con estos Script.
"""

import random
import math

from libs.mis_decoradores import tiempo_ejecucion_

from extras import distance as norma
from constantes import *


@tiempo_ejecucion_
def gen_distance_matrix(vertex_list=[]):
    """
        Genera la matrix triangular inferior con las distancias entre los
        diferentes puntos o vertices o si se quiere Nodos..

        Nota: por el momento este metodo no soporta numpy

        Parametros Entrada:
            vertex_list : lista con las posiciones x,y de todos los vertices
                          del problema
        Devuelve:
            distance_matrix : Matrix triangular inferior con la distancia
                              euclidea que hay entre todos los vertices del
                              problema tsp.
    """
    distance_matrix = []

    for vertex_i in vertex_list[1:]:
        lista = []
        for vertex_j in vertex_list[:vertex_list.index(vertex_i)]:
            dista = norma(vertex_i, vertex_j)
            lista.append(dista)
        distance_matrix.append(lista)

    return distance_matrix


@tiempo_ejecucion_
def gen_distance_matrix_(vertex_list=[], dist_type=EUC_2D):
    """
        Genera la matrix triangular inferior con las distancias entre los
        diferentes puntos o vertices o si se quiere Nodos..

        Nota: por el momento este metodo no soporta numpy

        Parametros Entrada:
            vertex_list : lista con las posiciones x,y de todos los vertices
                          del problema
        Devuelve:
            distance_matrix : Matrix triangular inferior con la distancia
                              euclidea que hay entre todos los vertices del
                              problema tsp

        Nota: version anterior, se mantiene solo por compatibilidad
    """
    distance_matrix = []

    for vertex_i in vertex_list[1:]:
        lista = []
        for vertex_j in vertex_list[:vertex_list.index(vertex_i)]:
            lista.append(norma(vertex_i, vertex_j, dist_type))
        distance_matrix.append(tuple(lista))

    return tuple(distance_matrix)


def distance(i=0, j=0, distance_matrix=[]):
    """
        retorna la distancia entre los vertices i y j utilizando la matrix de
        distancias.

        Parametros Entrada:
            i,j : vectores i,j del problema de TSP
            distance_matrix : matrix triangular inferior que contiene las
                              distancias entre todos los vectores del problema.
    """
    if i < j:
        return distance_matrix[j-1][i]

    elif i > j:
        return distance_matrix[i-1][j]

    else:
        return 0


def update_matrix(value=0, i=0, j=0, matrix=[]):
    """
        Para hacer updates en la memoria
    """
    if i == j:
        return False

    elif i < j:
        matrix[j-1][i] = value
        return True

    elif i > j:
        matrix[i-1][j] = value
        return True


#@tiempo_ejecucion_
def get_obj_function_value(solution=[], distance_matrix=[]):
    """
        Calcular el valor total (suma distancias entre todos los vertices) de
        una funcion objectivo (solucion)

        Parametros Entrada:
            solution : array con el listado de vertices de una solucion del
                        problema de tsp, el listado se refiere a los indices
                        de los vertices.
            distance_matrix : matrix triangular inferior que contiene las
                              distancias entre todos los vectores del problema.
    """
    funtion_obj = 0
    n_vertex = len(solution)
    #sumo las distancia entre todos los vertices consecutivos de la solucion
    for i in xrange(n_vertex-1):
        vert_i = solution[i]
        vert_j = solution[i+1]
        funtion_obj += distance(vert_i, vert_j, distance_matrix)

    #por ultimo sumo la distancia que hay entre el primer y ultimo vertice
    funtion_obj += distance(solution[n_vertex-1], solution[0], distance_matrix)

    return funtion_obj


@tiempo_ejecucion_
def gen_random_sol(vertex_list_=[]):
    """
        genera una solucion al azar, para el problema de tsp

        Parametros Entrada:
            vertex_list_ : representa la lista todos los vertices o nodos que
            componen el problema de TSP
    """
    random.seed() #colocamos la semilla
    n_vertex = len(vertex_list_)
    vertex_list = range(n_vertex)
    random_sol = []
    while vertex_list != []:
        vertex = random.choice(vertex_list)
        vertex_list.pop(vertex_list.index(vertex))
        random_sol.append(vertex)

    return random_sol


def create_memory(size):
    """
        Genera una matriz que representa la memoria de largo plazo
    """
    memory = []
    for i in xrange(1,size):
        row = [0]*i
        #for j in xrange(i):
        #   row.append(0)
        memory.append(row)
    return memory


def update_memory(memory, solution, maximum=0):
    """
        Actualiza la memoria, es decir toma a solución y toma los nodos
        de a pares (como indices de la matriz) y aumenta en uno el
        contador de ocurrencia de una union de nodos en la matriz.
    """
    previo = solution[0]
    for actual in solution[1:]:
        counter = distance(previo,actual,memory)
        counter = counter+1
        if counter > maximum:
            maximum = counter
        update_matrix(counter,previo,actual,memory)
        previo = actual
    #aun cuando se modifique memory, maximum no lo ara
    return memory, maximum

