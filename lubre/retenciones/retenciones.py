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

# contador de iteraciones
contador = 1

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
	

def Lubre():
    global contador

    # Leer archivo CSV con DictReader() y filtrar salida
    with open('reporte.csv') as csvarchivo:
        entrada = csv.DictReader(csvarchivo, delimiter=';', quoting=csv.QUOTE_NONE)
        for reg in entrada:
            # descartamos las operaciones de tipo TRANS
            if reg['TIPO_OPERA'] != 'TRANS':
                if reg['CUIT'] == '':
                    print('Cliente sin CUIT', reg['NOMBRE'], reg['NUMERO'])
                    break
                else:
                    # verificamos que el campo percepcion sea distinto de cero
                    if validar_importe(reg['IMPORTE']) != 0:
                        print(jurisdiccion(reg['CUIT']) + 
                              reg['CUIT'] + 
                              validar_fecha(reg['FECHA']) +
                              '0'.rjust(4, '0') + 
                              str(contador).rjust(16, '0') + 
							  'F' + # validar_comprobante(reg['TIPOCOMP']) + 
							  'A' + # reg['LETRA'] + 
                              '0'.rjust(20, '0') +
                              reg['IMPORTE'].rjust(11, '0')
                        )
                        contador = contador + 1

def Mayor():
    global contador
    
    # Leer archivo CSV con DictReader() y filtrar salida
    with open('reporte-2.csv') as csvarchivo:
        entrada = csv.DictReader(csvarchivo, delimiter=';', quoting=csv.QUOTE_NONE)
        for reg in entrada:
            if reg['Operacion'] == 'FACPRO':
                # verificamos que el campo Importe sea distinto de cero
                if validar_importe(reg['Importe']) != 0:
                    print(jurisdiccion(reg['CUIT']) + 
                          reg['CUIT'] + 
                          validar_fecha(reg['Fecha']) +
                          '0'.rjust(4, '0') + 
                          str(contador).rjust(16, '0') + 
						  'F' + # validar_comprobante(reg['TIPO_COMP']) + 
						  'A' + # reg['LETRA'] + 
                          '0'.rjust(20, '0') +
                          reg['Importe'].rjust(11, '0')
                    )
                    contador = contador + 1


if __name__ == '__main__':
    Lubre()
    Mayor()
