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

# apertura del archivo ascii para escritura
f = open('3.CITI-Ventas.txt', 'w')
f2 = open('4.CITI-Ventas-Alicuotas.txt', 'w')

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


def validar_operacion(valor1, valor2):
    if valor1 == valor2:
        return 'N'
    else:
        return '0'


def validar_neto_gravado(gravado, no_gravado):
    if gravado == no_gravado:
        return validar_total(gravado)
    else:
        return validar_total('0')


def validar_alicuota_iva(iva, otro):
    iva = validar_importe(iva)
    otro = validar_importe(otro)
    if iva != 0:
        return '3'
    elif otro != 0:
        return '4'
    else:
        return '5'


def validar_iva(iva, otro):
    iva = validar_importe(iva)
    otro = validar_importe(otro)
    if iva != 0:
        return validar_total(iva)
    elif otro != 0:
        return validar_total(otro)
    else:
        return validar_total(0)


def imprimir_linea(reg):
    f.write(validar_fecha(reg['FECHA']) +
            validar_comprobante(reg['TIPOCOMPROB'] + reg['LETRA']) +
            reg['TERMINAL'].rjust(5, '0') +
            reg['NUMERO'].rjust(20, '0') +
            reg['NUMERO'].rjust(20, '0') +
            '80' +
            reg['CUIT'].replace('-', '').rjust(20, '0') +
            reg['NOMBRE'][0:30].ljust(30, ' ') +
            validar_total(reg['TOTAL']) +
            validar_total(reg['NOGRAVA']) +
            '0'.rjust(15, '0') +
            '0'.rjust(15, '0') +
            validar_total(reg['PERCIVA']) +
            '0'.rjust(15, '0') +
            '0'.rjust(15, '0') +
            validar_total(reg['IMPINT']) +
            'PES' +
            '0001000000' +
            '1' +
            validar_operacion(reg['NOGRAVA'], reg['TOTAL']) +
            '0'.rjust(15, '0') +
            validar_fecha(reg['FECHA'])
    )


def imprimir_linea_alicuota(reg):
    f2.write(validar_comprobante(reg['TIPOCOMPROB'] + reg['LETRA']) +
             reg['TERMINAL'].rjust(5, '0') +
             reg['NUMERO'].rjust(20, '0') +
             validar_neto_gravado(reg['GRAVADO'], reg['NOGRAVA']) + 
             validar_alicuota_iva(reg['IVA21'], reg['OTROIVA']) + 
             validar_iva(reg['IVA21'], reg['OTROIVA'])
    )

def lubre():
    with open('citi-ventas.csv') as csvarchivo:
        entrada = csv.DictReader(csvarchivo,
                                 delimiter=';',
                                 quoting=csv.QUOTE_NONE)
        for (contador, reg) in enumerate(entrada):
            try:
                if contador > 0:
                    # salto de línea en el archivo
                    # lo hago aquí para evitar el último salto de línea
                    f.write('\n')
                    f2.write('\n')
                imprimir_linea(reg)
                imprimir_linea_alicuota(reg)
            except BaseException:
                print('Error al procesar linea número ', contador + 2)
                raise


if __name__ == "__main__":
    try:
        limpiar()
        lubre()
        print('Archivo {} creado correctamente.'.format('3.CITI-Ventas y 4.CITI-Ventas-Alicuotas'))
    except ErrorRangoFecha as err:
        print('La fecha {} no pertenece al rango {}-{}'.format(err.fecha, err.inicio, err.fin))
    finally:
        f.close()
        f2.close()
