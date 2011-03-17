#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Version: 0.0.6 (Beta)

    Autor: Ricardo D. Quiroga->L2Radamanthys

    Fecha: 08 de Junio de 2010

    E-mail:
        l2radamanthys@gmail.com
        l2radamanthys@saltalug.org.ar
        ricardoquiroga.dev@gmail.com

    SitioWeb:
        http://www.l2radamanthys.com.ar
        http://l2radamanthys.blogspot.com

    Descripcion:
        Sencillo modulo para cargar los problemas y soluciones de la libreria
        TSPLib.

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

import sys

from libs.mis_decoradores import tiempo_ejecucion_

from extras import echo
from constantes import *


@tiempo_ejecucion_
def tsp_load(file_name='', use_numpy=False, use_path=False):
    """
        Mi version :P, del codigo para cargar los problemas de TCP, ademas
        opcionalmente permite convertir a un array de la libreria Numpy.
        como todos los archivos que vi (aunque no lei exaustivamente la info
        sobre como estan formateados) estan bien formados omitire algunas
        comprobaciones sobre identificadores.

        Parametros Entrada:
            file_name : nombre del archivo o la  ruta del mismo
            use_numpy : (bool), si se devovera un array normal o un objecto
                        numpy
            use_path : (bool)si se usara la ruta de los problemas para el
                        fichero a cargar, en caso contrario la ruta del mismo
                        devera ser pasada en file_name

        Devuelve:
            name : nombre del problema
            comment : comentarios
            point_list: lista de puntos
    """
    #Inclui un directorio con todos los problemas descargados de TSPLib por
    #lo que solo tendran que colocar en True 'use_path' y colocar solo el
    #nombre del fichero del problema
    if use_path:
        path = os.path.join(PROB_DIR, file_name)
    else:
        path = file_name

    #comprobacion de que el fichero exista en la ruta que pasamos
    try:
        file = open(path, 'r')
    except IOError, e:
        echo('Error no se pudo cargar el fichero %s' %path)
        exit(1)

    data = file.readlines()
    file.close()

    #estraigo el nombre del problema
    name = data[0].split(": ")[1][:-1]

    id = 1
    comment = ''
    #busqueda de la la cadena de comentarios
    loop = True
    while loop:
        if 'COMMENT' in data[id]:
            comment = data[1].split(": ")[1][:-1]
            loop = False

        elif 'NODE_COORD_SECTION' in data[id]:
            loop = False

        else:
            id += 1

    #busqueda de la linea NODE_COORD_SECTION
    loop = True
    while loop:
        if 'NODE_COORD_SECTION' in data[id]:
            loop = False
        id += 1

    #omito la linea que dice NODE_COORD_SECTION y la ultima linea EOF
    data_points = data[id:-1]

    point_list = [] #lista de  puntos x,y que representaran los vertices
    for linea in data_points:
        #obtengo las posiciones de los vertices o nodos, split por defecto
        #separara por saltos de linea \n y espacios en blanco ' '
        num = linea.split()
        tupla = float(num[1]), float(num[2])
        point_list.append(tupla)
        #v = Vector2D(float(num[1]), float(num[2]))
        #point_list.append(v)

    #pregunta si se devolvera un objecto array de numpy o un array tradicional
    #por ende requiere tener Numpy instalado :P
    if use_numpy and NUMPY_OK:
        point_list = np.array(point_list, np.float)

    echo('Cantidad de Vertices del problema %s: %s' %(name, len(point_list)))
    return name, comment, point_list


def tsp_load_(file_name='', use_path=False):
    """
        funcion ampliada, la cual lanzara un error si se intenta cargar un
        archivo con tipo de distancia Explicito. como el uso de numpy no esta
        soportado completamente el mismo esta desactivado

        Devuelve:
            name : nombre del problema
            comment : comentarios
            dist_type: tipo de distancia que se usa
            point_list: lista de puntos
    """
    #Inclui un directorio con todos los problemas descargados de TSPLib por
    #lo que solo tendran que colocar en True 'use_path' y colocar solo el
    #nombre del fichero del problema
    if use_path:
        path = os.path.join(PROB_DIR, file_name)
    else:
        path = file_name

    #comprobacion de que el fichero exista en la ruta que pasamos
    try:
        file = open(path, 'r')
    except IOError, e:
        echo('Error no se pudo cargar el fichero %s' %path)
        exit(1)

    data = file.readlines()
    file.close()

    #estraigo el nombre del problema
    name = data[0].split(": ")[1][:-1]
    comment = ''
    dist_type = 'EUC_2D'
    data_type = 'COORD_DISPLAY'

    ini = 1
    loop = True
    while loop:
        if 'COMMENT' in data[ini]:
            comment = data[ini].split(": ")[1][:-1]

        elif 'EDGE_WEIGHT_TYPE' in data[ini]:
            dist_type = data[ini].split(": ")[1][:-1]

        elif 'DISPLAY_DATA_TYPE' in data[ini]:
            data_type = data[ini].split(": ")[1][:-1]

        if 'NODE_COORD_SECTION' in data[ini]:
            loop = False

        if 'EDGE_WEIGHT_SECTION' in data[ini]:
            loop = False

        ini += 1

    if WEIGHT_TYPES[dist_type] != EUC_2D:
        echo('Cuidado - El tipo de distancia usado no es la Euclidea..!')

    if WEIGHT_TYPES[dist_type] == EXPLICIT:
        echo("Error - Tipo de Distancia no soportado")
        sys.exit(1)

    #busco si la ultima linea es la cadena EOF para omitirla
    if 'EOF' in data[-1]:
        data_points = data[ini:-1]
    else:
        data_points = data[ini:]

    point_list = [] #lista de  puntos x,y que representaran los vertices
    for linea in data_points:
        #obtengo las posiciones de los vertices o nodos, split por defecto
        #separara por saltos de linea \n y espacios en blanco ' '
        num = linea.split()
        tupla = float(num[1]), float(num[2])
        point_list.append(tupla)

    #pregunta si se devolvera un objecto array de numpy o un array tradicional
    #por ende requiere tener Numpy instalado :P
    #if use_numpy and NUMPY_OK:
    #    point_list = np.array(point_list, np.float)

    echo('Cantidad de Vertices del problema %s: %s' %(name, len(point_list)))
    return name, comment, WEIGHT_TYPES[dist_type], point_list


@tiempo_ejecucion_
def tsp_sol_load(file_name='', use_numpy=False, use_path=False):
    """
        Esta funcion permite cargar las soluciones optimas de algunos de los
        los problemas que vienen con la TSPLib (no todos tienen solucion
        optima). La misma acepta los mismos parametros que tsp_load()

        Parametros Entrada:
            file_name : nombre del archivo o la  ruta del mismo
            use_numpy : (bool), si se devovera un array normal o un objecto
                        numpy
            use_path : (bool)si se usara la ruta de las soluciones para el
                        fichero a cargar, en caso contrario la ruta del mismo
                        devera ser pasada en file_name

        Devuelve:
            prob_file : nombre del fichero '.tsp' del cual este archivo es
                        solucion
            soluc_opt: solucion optima, listado de nodos (indice de cada nodo)
    """
    #Inclui un directorio con todos las soluciones optimas descargados desde
    #TSPLib, por lo que solo tendran que colocar en True 'use_path' y colocar
    #solo el nombre del fichero
    if use_path:
        path = os.path.join(SOLUC_DIR, file_name)
    else:
        path = file_name

    #comprobacion de que el fichero exista en la ruta que pasamos
    try:
        file = open(path, 'r')
    except IOError, e:
        echo('Error no se pudo cargar el fichero %s' %path)
        exit(1)

    data = file.readlines()
    file.close()

    #nombre del archivo que contiene el problemas
    prob_file = os.path.split(data[0].split(" : ")[1][:-1])[-1][:-11]

    #algunos no incluyen la extencion del archivo
    if not('tsp' in prob_file):
        prob_file += '.tsp'

    #buscamos el comienzo de la lista con la solucion optima
    ini = 1
    loop = True
    while loop:
        if 'TOUR_SECTION' in data[ini]:
            loop = False
        ini += 1

    if 'EOF' in data[-1]:
        fin = -2
    else:
        fin = -1

    #convierto todos los valores a enteros
    soluc_opt = [int(vertex_id)-1 for vertex_id in data[ini:fin]]
    return prob_file, soluc_opt
