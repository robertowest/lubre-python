#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import calendar, datetime
import operator
import argparse

from datetime import date, timedelta 

# obtenemos primera y ultima fecha del mes anterior
hoy = date.today()
prev = hoy.replace(day=1) - timedelta(days=1) 
inicioMes = "{}/{}/{}".format(1, prev.month, prev.year)
finMes = "{}/{}/{}".format(calendar.monthrange(prev.year, prev.month)[1], prev.month, prev.year)

# matriz de jurisdiccion
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

def validar_importe(valor):
    return float(valor.replace(',','.'))
	
def validar_fecha(valor):
	fecha = datetime.datetime.strptime(valor, '%d/%m/%Y').strftime('%d/%m/%Y')
	return fecha

def validar_comprobante(valor):
    switcher = {
        'FAC': 'F',
		'FT': 'F',
        'NC': 'C',
        'NCR': 'C',
		'ND': 'D',
		'NDE': 'D',
		'REC': 'R',
    }
    return switcher.get(valor, "F")

def validar_total(valor):
    total = validar_importe(valor)
    if total < 0:
        valor = '-' + str(abs(total)).rjust(10, '0')
    else:
        valor = str(total).rjust(11, '0')
    return valor.replace(".", ",")

def Percepciones():
    with open('reporte.csv') as csvarchivo:
        entrada = csv.DictReader(csvarchivo, delimiter=';', quoting=csv.QUOTE_NONE)
        for reg in entrada:
            # verificamos que el campo percepcion sea distinto de cero
            if validar_importe(reg['PERC_IB']) != 0:
                print(jurisdiccion(reg['CUIT']) + 
                      reg['CUIT'] + 
                      validar_fecha(reg['FECHA']) +
                      reg['TERMINAL'].rjust(4, '0') + 
                      reg['NUMERO'].rjust(16, '0') + 
                      'F' + reg['LETRA'] +
                      reg['TOTAL'].rjust(11, '0')
                )

def PercepDEBO():
    # gestion
    with open('reporte-debo.csv') as csvarchivo:
        entrada = csv.DictReader(csvarchivo, delimiter=';', quoting=csv.QUOTE_NONE)
        for reg in entrada:
            # verificamos que el campo percepcion sea distinto de cero
            if validar_importe(reg['Per.I.Btos.']) != 0:
                print(jurisdiccion(reg['CUIT']) + 
                      reg['CUIT'][3:] + 
                      validar_fecha(reg['Fecha']) +
                      reg['N. Comprobante'][5:9] + 
                      reg['N. Comprobante'][10:].rjust(16, '0') + 
                      validar_comprobante(reg['N. Comprobante'][:2]) + 
                      reg['N. Comprobante'][3:4] +
                      validar_total(reg['Total'])
                )

Percepciones()
PercepDEBO()
