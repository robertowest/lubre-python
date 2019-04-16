#! usr/bin/python
# -*- coding: utf-8 -*-

import os


def obtener_estructura(archivo):
    try:
        fichero = open(archivo, 'r')
        registro = []

        for linea in fichero.readlines():
            registro.append(linea.rstrip('\n').split(','))

    except BaseException:
        registro = []

    finally:
        fichero.close()
    
    return registro


def valor(linea, estructura):
    try:
        desde = int(estructura[1]) - 1
        hasta = int(estructura[2])
        valor = linea[desde:hasta]

    except BaseException:
        valor = 'error'

    return valor


def leer_archivo(archivo, estructura):
    try:
        fichero = open(archivo, 'r')
        registro = []

        for linea in fichero.readlines():
            for i in range(len(estructura)):
                print('{}: {}'.format(estructura[i][0].rjust(26, ' '), 
                                      valor(linea, estructura[i])))
            print('-----')
            # os.system("Pause")

    except BaseException:
        registro = []

    finally:
        fichero.close()

if __name__ == "__main__":
    estructura = obtener_estructura('compras.txt')
    leer_archivo('iva_compras.txt', estructura)
