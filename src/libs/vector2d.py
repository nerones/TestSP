#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
vector2d.py
============
    Version: 0.0.4 (Beta)

    Autor: Ricardo Daniel Quiroga -> L2Radamanthys

    Fecha: 15 de Febrero de 2010

    E-mail:
        l2radamanthys@gmail.com
        ricardoquiroga.dev@gmail.com
        l2radamanthys@saltalug.org.ar

    Web:
        http://www.l2radamanthys.com.ar
        http://l2radamanthys.blogspot.com

    Descripcion:
        Libreria con varias Funciones Matematicas ampliadas. que ademas soporta
        trabajar con un objecto vector2d

    Terminos y Condiciones:
        Este Script es Sofware Libre y esta vajo terminos de la GNU General
        Public Licence publicada por la Free Sofware Foundation
        (http://www.fsf.org) version 2 de la licencia o puede opcinalmente
        usar versiones posteriores de la licencia.

        Usted puede redistribuir y/o modificar este Script
        siguiendo los terminos de la GNU General Public Licence
        para mayor informacion lease la copia de la licencia que
        se adjunta con estos script.
"""

__version__ = "0.0.4-Beta"
__autor__ = "Ricardo D. Quiroga - L2Radamanthys  l2radamanthys@gmailcom"
__date__ = "15 de Febrero de 2010"
__copyright__ = "Copyright (c) 2010 Ricardo D. Quiroga"
__license__ = "GPL2"


import math

from constantes import *


class Vector2D(object):
    """
        Clase que simula un vector de 2 dimenciones, permite operaciones
        matematicas de manera directa.
    """
    def __init__(self, x_tup=None, y=None):
        """
            Cosntructor de la clase vector 2D.
        """
        if x_tup != None and y != None:
            self.__x = float(x_tup)
            self.__y = float(y)
        elif x_tup != None and y == None:
            self.__x = float(x_tup[0])
            self.__y = float(x_tup[1])
        else:
            self.__x = 0.0
            self.__y = 0.0


    def get_x(self):
        """
            Retorna el valor x
        """
        return self.__x


    def get_y(self):
        """
            Retorna el valor de y
        """
        return self.__y


    def set_x(self, val):
        """
            Metodo para defir explicitamente el valor, del atributo x
        """
        self.__x = float(val)


    def set_y(self, val):
        """
            Metodo para defir explicitamente el valor, del atributo y
        """
        self.__y = float(val)


    def __get(self):
        """
            Retorna la posicion como valor entero
        """
        return (int(round(self.__x)), int(round(self.__y)))


    def __set(self, pos):
        """
           Define el valor del vector  pasando una tupla como parametro.
        """
        self.__x = float(pos[0])
        self.__y = float(pos[1])


    pos = property(__get, __set, None, "Define el valor mediante una tupla")


    def zero(self):
        """
            Convierte en nulo el valor del vector.
        """
        self.__x = 0.0
        self.__y = 0.0


    def length(self):
        """
            Retorna la longitud del vector.
        """
        return math.sqrt(self.__x ** 2 + self.__y ** 2)

    def length_sq(self):
        """
            Retorna la longitud del vector al cuadrado.
        """
        return (self.__x ** 2 + self.__y ** 2)


    def norma(self):
        """
            Retorna la norma euclidea, que es equivalenete a la longitud del
            vector.
        """
        return self.length()


    def normalizar(self):
        """
            normaliza el vector
        """
        vect_len = self.length()
        self.__x /= vect_len
        self.__y /= vect_len


    def normalizado(self):
        """
            Retorna una copia del vector normalizado
        """
        vect_len = self.length()
        return Vector2D(self.__x / vect_len, self.__y / vect_len)


    def copy(self):
        """
            Retorna una copia del vector
        """
        return Vector2D(self.__x, self.__y)


    def punto(self, vect):
        """
            Calcula el Producto Punto
        """
        return Vector2D(self.__x * vect[0], self.__y * vect[1])


    def signo(self, vect):
        """
            Retorna True si el vector esta en sentido horario
        """
        if self.__y * vect[0] > self.__x * vect[1]:
            return False
        else:
            return True


    def perp(self):
        """
            Petorna un vector perpendicular a este
        """
        return Vector2D(-self.__y, self.__x)


    def truncate(self, max):
        """
        """
        if self.length() > max:
            self.normalizar()
            self *= max


    def distancia(self, vect):
        """
            Retorna la distancia euclidea entre los 2 vectores
        """
        dx = self.__x - vect[0]
        dy = self.__y - vect[1]
        return math.sqrt(dx**2 + dy**2)


    def distancia_sq(self, vect):
        """
            Retorna la distancia euclidea entre los 2 vectores
            al cuadrado
        """
        dx = self.__x - vect[0]
        dy = self.__y - vect[1]
        return dx**2 + dy**2


    def reflect(self, vect):
        """
            Proyecta el vector sobre otro
        """
        self += 2.0 * self.punto(vect) * vect.get_reverse()


    def get_reverse(self):
        """
            Retorna el vector inverso
        """
        return -vect


    #--------------------otros-------------------------#
    def __getitem__(self, key):
        if key == 0 or key == 'x':
            return self.__x
        elif key == 1 or key == 'y':
            return self.__y


    def __setitem__(self, key, value):
        if key == 0 or key == 'x':
            self.__x = value
        elif key == 1 or key == 'y':
            self.__y = value


    def __repr__(self):
        """
            Convercion a String para representar el objecto
        """
        return "Vector2D(%f, %f)" %(self.__x, self.__y)


    def __len__(self):
        return 2


    #------------operaciones aritmeicas-------------------#
    #sobrecarga de la Suma
    def __add__(self, otr):
        vect = Vector2D()

        if isinstance(otr, Vector2D): #si son del mismo tipo
            vect.set_x(self.__x + otr[0])
            vect.set_y(self.__y + otr[1])

        elif hasattr(otr, "__getitem__"): #si el otro obj es una lista
            vect.set_x(self.__x + otr[0])
            vect.set_y(self.__y + otr[1])

        else: #valor atomico
            vect.set_x(self.__x + otr)
            vect.set_y(self.__y + otr)

        return vect


    __radd__ = __add__


    def __iadd__(self, otr):
        """
        """
        if isinstance(otr, Vector2D): #si son del mismo tipo
            self.__x += otr[0]
            self.__y += otr[1]

        elif hasattr(otr, "__getitem__"): #si el otro obj es una lista
            self.__x += otr[0]
            self.__y += otr[1]

        else: #valor atomico
            self.__x += otr
            self.__y += otr

        return self


    #sobrecarga de la Resta
    def __sub__(self, otr):
        """
            Sobrecarga del operador resta
        """
        vect = Vector2D()

        if isinstance(otr, Vector2D): #si son del mismo tipo
            vect.set_x(self.__x - otr[0])
            vect.set_y(self.__y - otr[1])

        elif hasattr(otr, "__getitem__"): #si el otro obj es una lista
            vect.set_x(self.__x - otr[0])
            vect.set_y(self.__y - otr[1])

        else: #valor atomico
            vect.set_x(self.__x - otr)
            vect.set_y(self.__y - otr)

        return vect


    __rsub__ = __sub__


    def __isub__(self, otr):
        """
        """
        if isinstance(otr, Vector2D): #si son del mismo tipo
            self.__x -= otr[0]
            self.__y -= otr[1]

        elif hasattr(otr, "__getitem__"): #si el otro obj es una tupla o lista
            self.__x -= otr[0]
            self.__y -= otr[1]

        else: #valor atomico
            self.__x -= otr
            self.__y -= otr

        return self


    #sobrecarga de la Multiplicacion
    def __mul__(self, otr):
        vect = Vector2D()

        if isinstance(otr, Vector2D): #si son del mismo tipo
            return (self.__x * otr[0] + self.__y * otr[1])

        elif hasattr(otr, "__getitem__"): #si el otro obj es una lista
            return (self.__x * otr[0] + self.__y * otr[1])

        else: #valor atomico
            vect.set_x(self.__x * otr)
            vect.set_y(self.__y * otr)
            return vect


    __rmul__ = __mul__


    def __imul__(self, otr):
        """
            solo se puede multiplicar por un escalar
        """
        if isinstance(otr, Vector2D): #si son del mismo tipo
            self.__x *= otr[0]
            self.__y *= otr[1]

        elif hasattr(otr, "__getitem__"): #si el otro obj es una lista
            self.__x *= otr[0]
            self.__y *= otr[1]

        else: #valor atomico
            self.__x *= otr
            self.__y *= otr

        return self


    #sobrecarga de la Divicion
    def __div__(self, otr):
        vect = Vector2D()

        if isinstance(otr, Vector2D): #si son del mismo tipo
            vect.set_x(self.__x / otr[0])
            vect.set_y(self.__y / otr[1])

        elif hasattr(otr, "__getitem__"): #si el otro obj es una lista
            vect.set_x(self.__x / otr[0])
            vect.set_y(self.__y / otr[1])

        else: #valor atomico
            vect.set_x(self.__x / otr)
            vect.set_y(self.__y / otr)

        return vect


    def __idiv__(self, otr):
        if isinstance(otr, Vector2D): #si son del mismo tipo
            self.__x /= otr[0]
            self.__y /= otr[1]

        elif hasattr(otr, "__getitem__"): #si el otro obj es una lista
            self.__x /= otr[0]
            self.__y /= otr[1]

        else: #valor atomico
            self.__x /= otr
            self.__y /= otr

        return self


    #-------------operaciones unarias-------------------#
    def __neg__(self):
        return Vector2D(-self.__x, -self.__y)


    def __pos__(self):
        return Vector2D(+self.__x, +self.__y)


    def __abs__(self):
        return Vector2D(abs(self.__x), abs(self.__y))


    def __invert__(self):
        return Vector2D(~self.__x, ~self.__y)


    #------------------comparacion----------------------#
    def __eq__(self, vect):
        if (vect[0] == self.__x) and (vect[1] == self.__y):
            return True
        else:
            return False


    def __neq__(self, vect):
        if (vect[0] != self.__x) or (vect[1] != self.__y):
            return True
        else:
            return False


#-------------- Varias Funciones Utiles -----------------------#
def angulo_r(vect_a, vect_b):
    """
        Retorna el angulo entre 2 vectores en radianes
    """
    a = Vector2D(vect_a[0], vect_a[1])
    b = Vector2D(vect_b[0], vect_b[1])

    sup = a * b
    inf = a.length() * b.length()
    try:
        tita = math.acos(sup / inf)
    except:
        tita = 0.0
    return tita


def angulo_g(vect_a, vect_b):
    """
        Retorna el angulo entre 2 vectores en grados
    """
    return math.degrees(angulo_r(vect_a, vect_b))


def angulo_pq(pto_a, pto_b):
    """
        Retorna el angulo que se forma entre 2 puntos cualesquiera en grados
    """
    u = Vector2D(pto_b[0], pto_b[1]) - Vector2D(pto_a[0], pto_a[1])
    v = Vector2D(100, 0)
    angulo = angulo_g(u, v)
    if pto_a[1] < pto_b[1]:
        return (360.0 - angulo) % 360
    else:
        return angulo % 360


def distancia(pto_a, pto_b):
    """
        Calcula la distancia euclidea entre 2 puntos cualesquiera
    """
    dx = pto_a[0] - pto_b[0]
    dy = pto_a[1] - pto_b[1]
    return math.sqrt(dx ** 2 + dy ** 2)


def wrap_arround(vect, max_x, max_y):
    """
        Trata una ventana como un toroide
    """
    if vect[0] > max_x:
        vect[0] = 0.0
    if vect[0] < 0:
        vect[0] = float(max_x)
    if vect[1] > max_y:
        vect[1] = 0.0
    if vect[1] < 0:
        vect[1] = float(max_y)


def not_inside_region(vect, top_left, bot_right):
    """
        Retorna Ttrue si el vector no esta dentro de una region en particular
        en caso contrario retorna False
    """
    return ((vect[0] < top_left[0] or vect[0] < bot_left[0]) or \
                (vect[1] < top_left[1] or vect[1] < bot_left[1]))


def inside_region(vect, top_left, bot_right):
    """
        Retorna true si el vector esta dentro de una region en particular
        en caso contrario retorna false
    """
    return not(not_inside_region(vect, top_left, bot_right))


def inside_region_(vect, left, top, right, botton):
    """
        Retorna true si el vector esta dentro de una region en particular
        en caso contrario retorna false
    """
    return not((vect[0] < left or vect[0] > right) or  \
            (vect[1] < top or vect[1] < botton))


def not_inside_region_(vect, left, top, right, botton):
    """
        Retorna true si el vector no esta dentro de una region en particular
        en caso contrario retorna false
    """
    return ((vect[0] < left or vect[0] > right) or  \
            (vect[1] < top or vect[1] < botton))
