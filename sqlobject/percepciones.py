#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import datetime
import operator
import argparse

catamarca = [''] # 903
jujuy = [''] # 910
la_rioja = [''] # 912
salta = [''] # 917
santiago = ['33-55565228-9'] # 922

# comprobamos a quien corresponde el CUIT
def jurisdiccion(valor):
    if valor in catamarca:
        cuit = '903'
    elif valor in jujuy:
        cuit = '910'
    elif valor in la_rioja:
        cuit = '912'
    elif valor in salta:
        cuit = '917'
    elif valor in santiago:
        cuit = '922'
    else:
        cuit = '924'
    
    return cuit

def Percepciones():
    # Leer archivo CSV con DictReader() y filtrar salida
    with open('PER_IBB_LUBRE.csv') as csvarchivo:
        entrada = csv.DictReader(csvarchivo, delimiter=';', quoting=csv.QUOTE_NONE)
        for reg in entrada:
            # verificamos que el campo percepcion sea distinto de cero
            if float(reg['PERC_IB'].replace(',','.')) != 0:
                # convertimos el campo fecha en formato dd/mm/yyyy
                print( jurisdiccion(reg['CUIT']) + 
                    reg['CUIT'] + 
                    datetime.datetime.strptime(reg['FECHA'], '%d/%m/%Y').strftime('%d/%m/%Y') +
                    reg['TERMINAL'].rjust(4, '0') + 
                    reg['NUMERO'].rjust(16, '0') + 
                    'F' + reg['LETRA'] +
                    reg['TOTAL'].rjust(11, '0')
                )
                # break


Percepciones()