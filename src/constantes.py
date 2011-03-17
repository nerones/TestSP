#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Conjunto de algunas constantes
"""

import os

#por algunas incompatibilidades con el codigo no se usara numpy
NUMPY_OK = False
#try:
#    import numpy as np
#    NUMPY_OK = True #indica que el modulo esta disponible
#except ImportError, e:
#    print "Error - El soporte para Numpy no esta instalado..."
#    NUMPY_OK = False #indica que el modulo no esta disponible

#directorio donde estan todos los problemas bajados de TSPLib
PROB_DIR = os.path.join('data', 'problemas')

#directorio donde estan todos la soluciones optimas descargadas de TSPLib
#nota: no todos los problemas planteados tienen solucion Optima
SOLUC_DIR = os.path.join('data', 'soluciones')

#listado de todos los archivos (Problemas) disponibles
PROB_LIST = os.listdir(PROB_DIR)


#------------------- tipos de distancias -------------------------#
EUC_2D = 0
EUC_3D = 1
MAN_2D = 2
MAN_3D = 3
MAX_2D = 4
MAX_3D = 5
GEO = 6
ATT = 7
CEIL_2D = 8
EXPLICIT = 9

WEIGHT_TYPES = {
    'EUC_2D' : 0,
    'EUC_3D' : 1,
    'MAN_2D' : 2,
    'MAN_3D' : 3,
    'MAX_2D' : 4,
    'MAX_3D' : 5,
    'GEO' : 6,
    'ATT' : 7,
    'CEIL_2D' : 8,
    'EXPLICIT' : 9,
}

