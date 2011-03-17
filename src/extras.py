#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Conjunto de funciones utiles
    fecha: 11 de Junio de 2010
"""

import os
import math
import pickle

from libs.mis_decoradores import captura_stdout

from constantes import *


def clear():
    """
        Sencilla funcion que permite limpiar la consola o terminal, tanto en
        GNU/Linux como Windows.
    """
    # GNU/Linux y Unix
    if os.name == 'posix':
        os.system('clear')
    # DOS y Windows
    elif os.name == 'dos' or os.name == 'nt':
        os.system('cls')
    #No definida para otros SO:'mac', 'os2', 'ce', 'java'
    else:
        print 'Error - clear() no esta implementada para este SO'


@captura_stdout
def echo(*argv, **kwargv):
    """
        funcion decorada para imprimir texto, funciona de manera muy similar a
        lo que es print, solo que agregando parentesis, ademas almacena la
        salida en un archivo normalmente llamado stdout.txt, el archivo sera
        creado en el directorio local si es que no existe.

        opcionalmente se puede expecificar explicitamente si se desea mostrar
        los elementos separados por salto de linea agregando el parametro
        jump=True al final. ejemplo:
            >>> echo('hola','mundo', jump=True)
    """

    salto = kwargv.get('jump', False)
    if salto:
        for ele in argv:
            print ele
    else:
        for ele in argv:
            print ele,
        print


def min_(k, vertex_list, dist_matrix=[]):
    """
        Calcula el vertice perteneciente a vertex_list mas cercano a k.

        Retorna
            ady_vertex : vertice mas cercano a k
            cost: costo de agregar el nuevo vertice
    """
    ady_vertex = None #vertice adyacente que se agregara
    cost = 9999999999 #defino un costo inicial muy elevado
    for vert in vertex_list: #bobo un algoritmo de busqueda
        if vert != k:
            ncost = dist(k, vert, dist_matrix)
            if ncost < cost:
                ady_vertex = vert
                cost = ncost
    return ady_vertex, cost


def load_solucion(file_name):
    """
        devuelve una solucion almacenada como array
    """
    file = open(file_name, 'rb')
    solucion = pickle.load(file)
    file.close()
    return solucion


def save_solucion(file_name, solucion):
    """
        guarda la solucion en un archivo
    """
    file = open(file_name, 'wb')
    pickle.dump(solucion, file)
    file.close()


def suma(n_o_vect=0):
    """
        Suma los elemenentos de un array o los valores de 0 a n  si se pasa
        un entero.
    """
    sum = 0
    #pregunta si es un obj iterable en fin un vector, tupla, dicionario
    #o cualquier otra cosa :P
    if hasattr(n_o_vect, "__getitem__"):
        for v in n_o_vect:
            sum += v
    #caso contrario tiene que ser un valor atomico osea un entero
    else:
        for i in xrange(n):
            sum += i
    return sum


#funciones de los diferentes tipos de distancias
def euc_2d(vertex_a, vertex_b):
    """
        Distancia Euclidea entre 2 vectores 2d redondeada a entero
    """
    dx = vertex_a[0] - vertex_b[0]
    dy = vertex_a[1] - vertex_b[1]
    return int(round(math.sqrt(dx*dx + dy*dy)))


def euc_3d(vertex_a, vertex_b):
    """
        Distancia Euclidea entre 2 vectores 3d redondeada a entero
    """
    dx = vertex_a[0] + vertex_b[0]
    dy = vertex_a[1] + vertex_b[1]
    dz = vertex_a[2] + vertex_b[2]
    return int(round(math.sqrt(dx*dx + dy*dy + dz*dz)))


def man_2d(vertex_a, vertex_b):
    """
        Distancia Manhattan entre 2 vectores 2d redondeada a entero
    """
    dx = abs(vertex_a[0] - vertex_b[0])
    dy = abs(vertex_a[1] - vertex_b[1])
    return int(round(dx + dy))


def man_3d(vertex_a, vertex_b):
    """
        Distancia Manhattan entre 2 vectores 3d redondeada a entero
    """
    dx = abs(vertex_a[0] - vertex_b[0])
    dy = abs(vertex_a[1] - vertex_b[1])
    dz = abs(vertex_a[2] - vertex_b[2])
    return int(round(dx + dy + dz))


def max_2d(vertex_a, vertex_b):
    """
        Distancia Maxima o Infinito entre 2 vectores 2d redondeada a entero
    """
    dx = abs(vertex_a[0] - vertex_b[0])
    dy = abs(vertex_a[1] - vertex_b[1])
    return int(max(dx, dy))


def max_3d(vertex_a, vertex_b):
    """
        Distancia Maxima o Infinito entre 2 vectores 2d redondeada a entero
    """
    dx = abs(vertex_a[0] - vertex_b[0])
    dy = abs(vertex_a[1] - vertex_b[1])
    dz = abs(vertex_a[2] - vertex_b[2])
    return int(round(max(dx, dy, dz)))


def att(vertex_a, vertex_b):
    """
        Distancia pseudo euclidea
    """
    dx = vertex_a[0] + vertex_b[0]
    dy = vertex_a[1] + vertex_b[1]
    rij = math.sqrt((dx*dx + dy*dy) / 10.0)
    tij = int(rij)
    if tij < rij:
        return (tij + 1)
    else:
        return tij


def geo(vertex_a, vertex_b):
    """
        Distancia Geografica
    """
    deg = int(vertex_a[0])
    min_ = vertex_a[0] - deg
    latitud_a = math.pi * (deg + 5.0 * min_ / 3.0) / 180.0
    deg = int(vertex_a[1])
    min_ = vertex_a[1] - deg
    longitud_a = math.pi * (deg + 5.0 * min_ / 3.0) / 180.0

    deg = int(vertex_b[0])
    min_ = vertex_b[0] - deg
    latitud_b = math.pi * (deg + 5.0 * min_ / 3.0) / 180.0
    deg = int(vertex_b[1])
    min_ = vertex_b[1] - deg
    longitud_b = math.pi * (deg + 5.0 * min_ / 3.0) / 180.0

    RRR = 6378.388 #supuestamente es el radio de la tierra
    q1 = math.cos(longitud_a - longitud_b)
    q2 = math.cos(latitud_a - latitud_b)
    q3 = math.cos(latitud_a + latitud_b)
    return  int(RRR * math.acos(0.5*((1.0 + q1)*q2-(1.0-q1)*q3))+1.0)


def ceil_2d(vertex_a, vertex_b):
    """
        Distancia Euclidea entre 2 vectores 2d redondeada a entero mas g
    """
    dx = vertex_a[0] + vertex_b[0]
    dy = vertex_a[1] + vertex_b[1]
    return int(round(math.sqrt(dx**2 + dy**2)))


def distance(vertex_a=(0,0), vertex_b=(0,0), dist_type=EUC_2D):
    """
        Funcion generica que viene a remplazar a las demas funciones de
        distancias
    """
    distances = {
        EUC_2D : euc_2d,
        EUC_3D : euc_3d,
        MAN_2D : man_2d,
        MAN_3D : man_3d,
        MAX_2D : max_2d,
        MAX_3D : max_3d,
        GEO : geo,
        ATT : att,
        CEIL_2D : ceil_2d,
        #EXPLICIT :
    }
    return distances[dist_type](vertex_a, vertex_b)


