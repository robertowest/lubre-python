#! usr/bin/python
# -*- coding: utf-8 -*-

import os
from datetime import date

clear = lambda : os.system('cls') # or clear for Linux

def limpiar():
    if os.name == "posix":
        os.system("clear")
    elif os.name == ("ce", "nt", "dos"):
        # os.system("cls")
        clear()

def iva_ventas():
    os.system('python iva_ventas.py')
    menu()

def iva_compras():
    os.system('python iva_compras.py')
    menu()

def menu():
    limpiar()

    print("----------------------------------------")
    print("--- Generación archivo CITI Reg.3685 ---")
    print("----------------------------------------")
    print("                     Version 1 Release 2")

    print('')
    print('Se procesará información del mes anterior a:', date.today().strftime("%B %Y"))
    print('')

    print("[1] Libro IVA Ventas")
    print("[2] Libro IVA Compras")
    print("[0] Salir")
 
    opcion = input("Ingresa una opción -> ")
 
    if opcion == "1":
        limpiar()
        iva_ventas()
    elif opcion == "2":
        limpiar()
        iva_compras()
    elif  opcion == "0":
        limpiar()
        exit()
    else:
        print("Opcion incorrecta")
        input()
        menu()


if __name__ == "__main__":
    menu()