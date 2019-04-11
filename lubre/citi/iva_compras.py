#! usr/bin/python
# -*- coding: utf-8 -*-

import calendar
import csv
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
    return float(valor.replace(',', '.'))


def validar_total(valor):
    total = validar_importe(valor)
    if total < 0:
        valor = '-' + str(abs(total)).replace(".", "").rjust(14, '0')
    else:
        valor = str(total).replace(".", "").rjust(15, '0')
    return valor


def alicuotas(*args):
    contador = 0
    for arg in args:
        if arg != 0:
            contador = contador + 1
    return str(contador)


def imprimir_linea(reg):
    print(
        validar_fecha(reg['FECHA']) +
        validar_comprobante(reg['TIPOCOMPROB'] + reg['LETRA']) +
        reg['TERMINAL'].rjust(5, '0') +
        reg['NUMERO'].rjust(20, '0') +
        '0'.rjust(16, '0') +
        '80' +
        reg['CUIT'].replace('-', '').rjust(20, '0') +
        reg['RAZON'].ljust(30, '0') +
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
        alicuotas(reg['IVA21'], reg['IVA10_5'], reg['IVA27']) +
        '0' +
        '0'.rjust(15, '0') +
        '0'.rjust(15, '0') +
        '0'.rjust(11, '0') +
        ' '.ljust(30, ' ') +
        '0'.rjust(15, '0')
    )


def lubre():
    with open('citi-compras.csv') as csvarchivo:
        entrada = csv.DictReader(csvarchivo,
                                 delimiter=';',
                                 quoting=csv.QUOTE_NONE)
        for (contador, reg) in enumerate(entrada):
            try:
                imprimir_linea(reg)
            except ValueError:
                print('Error al procesar linea número ', contador + 2)
                break
            except ErrorRangoFecha as err:
                print('La fecha {} no pertenece al rango {}-{}'.
                      format(err.fecha, err.inicio, err.fin))
                print('Error al procesar linea número ', contador + 2)
                break


def debo():
    pass


if __name__ == "__main__":
    limpiar()
    lubre()
