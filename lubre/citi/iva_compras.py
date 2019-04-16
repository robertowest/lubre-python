#! usr/bin/python
# -*- coding: utf-8 -*-

import calendar
import csv
# import pdb; pdb.set_trace()
import os

from argparse import ArgumentParser
from datetime import datetime
from datetime import date, timedelta

# ArgumentParser con una descripción de la aplicación
# (https://docs.python.org/2/library/argparse.html#argumentparser-objects)
parser = ArgumentParser(description='%(prog) generar archivo de texto')

# Argumento opcional. Si se pametriza, requiere acompañarlo de un valor
parser.add_argument('-mes', help='mes que desea procesar', type=int)

# Por último parsear los argumentos
args = parser.parse_args()


# obtenemos primera y ultima fecha del mes anterior
hoy = date.today()
prev = hoy.replace(day=1) - timedelta(days=1)

if args.mes:
    prev = datetime(prev.year, args.mes, 1)

inicioMes = datetime(prev.year, prev.month, 1)
finMes = datetime(prev.year, prev.month,
                  calendar.monthrange(prev.year, prev.month)[1])

# lista para alicuotas
alicuotas = []

# apertura del archivo ascii para escritura
nombre = '1.CITI-Compras.txt'
f = open(nombre, 'w')


class Error(Exception):
    """Clase base para excepciones en el módulo."""
    pass


class ErrorRangoFecha(Error):
    """Excepción lanzada por errores en las entradas.

    Atributos:
        expresion -- expresión de entrada en la que ocurre el error
        mensaje -- explicación del error
    """

    def __init__(self, fecha, inicio, fin):
        self.fecha = fecha
        self.inicio = inicio
        self.fin = fin


def limpiar():
    if os.name == "posix":
        os.system("clear")
    elif os.name == ("ce", "nt", "dos"):
        os.system("cls")


def validar_fecha(valor):
    try:
        fecha = datetime.strptime(valor, '%d/%m/%Y')
        if fecha >= inicioMes and fecha <= finMes:
            return fecha.strftime('%Y%m%d')
        else:
            raise ErrorRangoFecha(valor,
                inicioMes.strftime('%d/%m/%Y'),
                finMes.strftime('%d/%m/%Y'))
    except ValueError:
        print('La fecha {} no es correcta'.format(valor))


def validar_comprobante(valor):
    switcher = {
        'FACA': '001',
        'FACB': '006',
        'FACC': '011',
        'LSGA': '090',
        'NCRA': '003',
        'NCRB': '008',
        'NCRC': '013',
        'NDEA': '002',
        'NDEB': '007',
        'NDEC': '012',
    }
    return switcher.get(valor, "F")


def validar_importe(valor):
    valor = valor.replace(',', '.')
    return float(valor)


def validar_total(valor):
    if isinstance(valor, float):
        total = valor
    else:
        total = validar_importe(valor)

    if total < 0:
        total = abs(total)
        valor = '-' + format(total, '.2f').replace(".", "").rjust(14, '0')
    else:
        total = abs(total)
        valor = format(total, '.2f').replace(".", "").rjust(15, '0')
    return valor


def cantidad_alicuotas(*args):
    contador = 0
    for arg in args:
        if validar_importe(arg) != 0:
            contador = contador + 1
    return contador


def recalcular_compra(reg):
    neto21 = validar_importe(reg['IVA21']) / (21 / 100)
    neto10 = validar_importe(reg['IVA10_5']) / (10.5 / 100)
    neto27 = validar_importe(reg['IVA27']) / (27 / 100)

    grabado = neto21 + neto10 + neto27
    no_grabado = validar_importe(reg['GRAVADO']) - grabado

    reg['GRABADO'] = format(grabado, '.2f').replace(".", ",")
    reg['NOGRAVADO'] = format(no_grabado, '.2f').replace(".", ",")


def imprimir_linea(reg):
    # comprobamos si existen más de una alícuota de IVA en la línea
    if cantidad_alicuotas(reg['IVA21'], reg['IVA10_5'], reg['IVA27']) > 1:
        recalcular_compra(reg)

    f.write(validar_fecha(reg['FECHA']) +
            validar_comprobante(reg['TIPOCOMPROB'] + reg['LETRA']) +
            reg['TERMINAL'].rjust(5, '0') +
            reg['NUMERO'].rjust(20, '0') +
            ''.rjust(16, ' ') +
            '80' +
            reg['CUIT'].replace('-', '').rjust(20, '0') +
            reg['RAZON'][0:30].ljust(30, ' ') +
            validar_total(reg['TOTAL']) +
            validar_total(reg['NOGRAVADO']) +
            '0'.rjust(15, '0') +
            validar_total(reg['PERC_IB']) +
            '0'.rjust(15, '0') +
            validar_total(reg['PERC_IVA']) +
            '0'.rjust(15, '0') +
            '0'.rjust(15, '0') +
            'PES' +
            '0001000000' +
            str(cantidad_alicuotas(reg['IVA21'],
                                   reg['IVA10_5'],
                                   reg['IVA27'])) +
            '0' +
            '0'.rjust(15, '0') +
            '0'.rjust(15, '0') +
            '0'.rjust(11, '0') +
            ' '.ljust(30, ' ') +
            '0'.rjust(15, '0'))
    recalcular_alicuota(reg)


def recalcular_alicuota(reg):
    # creamos una lista para cada alicuota
    iva21 = {'Comprobante': validar_comprobante(reg['TIPOCOMPROB'] + reg['LETRA']),
             'Terminal': reg['TERMINAL'].rjust(5, '0'),
             'Numero': reg['NUMERO'].rjust(20, '0'),
             'Documento': '80',
             'CUIT': reg['CUIT'].replace('-', '').rjust(20, '0'),
             'Neto': validar_total(validar_importe(reg['IVA21']) / (21 / 100)),
             'Alicuota': '0005',
             'Iva': validar_total(reg['IVA21'])}

    iva10 = {'Comprobante': iva21['Comprobante'],
             'Terminal': iva21['Terminal'],
             'Numero': iva21['Numero'],
             'Documento': iva21['Documento'],
             'CUIT': iva21['CUIT'],
             'Neto': validar_total(validar_importe(reg['IVA10_5']) / (10.5 / 100)),
             'Alicuota': '0004',
             'Iva': validar_total(reg['IVA10_5'])}

    iva27 = {'Comprobante': iva21['Comprobante'],
             'Terminal': iva21['Terminal'],
             'Numero': iva21['Numero'],
             'Documento': iva21['Documento'],
             'CUIT': iva21['CUIT'],
             'Neto': validar_total(validar_importe(reg['IVA27']) / (27 / 100)),
             'Alicuota': '0003',
             'Iva': validar_total(reg['IVA27'])}

    # agregamos los nuevos elementos
    if validar_importe(iva21['Iva']) != 0:
        alicuotas.append(iva21)
    if validar_importe(iva10['Iva']) != 0:
        alicuotas.append(iva10)
    if validar_importe(iva27['Iva']) != 0:
        alicuotas.append(iva27)

    

def imprimir_alicuotas():
    f = open('2.CITI-Compras-Alicuotas.txt', 'w')

    for (contador, reg) in enumerate(alicuotas):
        if contador > 0:
            f.write('\n')
        f.write(reg['Comprobante'] +
                reg['Terminal'] +
                reg['Numero'] +
                reg['Documento'] +
                reg['CUIT'] +
                reg['Neto'] +
                reg['Alicuota'] +
                reg['Iva'])
    f.close()


def lubre():
    with open('citi-compras.csv') as csvarchivo:
        entrada = csv.DictReader(csvarchivo,
                                 delimiter=';',
                                 quoting=csv.QUOTE_NONE)
        for (contador, reg) in enumerate(entrada):
            try:
                if contador > 0:
                    # salto de línea en el archivo
                    # lo hago aquí para evitar el último salto de línea
                    f.write('\n')
                imprimir_linea(reg)
                recalcular_alicuota(reg)
            except BaseException:
                print('Error al procesar linea número ', contador + 2)
                raise
        
        imprimir_alicuotas()

def debo():
    pass


if __name__ == "__main__":
    try:
        limpiar()
        lubre()
        print('Archivo {} creado correctamente.'.format(nombre))
    except ErrorRangoFecha as err:
        print('La fecha {} no pertenece al rango {}-{}'.format(err.fecha, err.inicio, err.fin))
    finally:
        f.close()
