#!/usr/bin/env python
# -*- coding: utf-8 -*-
from argparse import ArgumentParser
 
# ArgumentParser con una descripción de la aplicación 
# (https://docs.python.org/2/library/argparse.html#argumentparser-objects)
parser = ArgumentParser(description='%(prog)s is an ArgumentParser demo')
 
# Argumento posicional. Los argumentos posicionales son obligatorios.
parser.add_argument('arg1')
 
# Un argumento posicional con una descripción 
parser.add_argument('arg2', help='help for arg2')
 
# Un argumento posicional con un tipo definido de tipo int 
# (https://docs.python.org/2/library/argparse.html#type)
parser.add_argument('arg3', help='help for arg3', type=int)
 
# Argumento posicional con tres opciones posibles 
# (https://docs.python.org/2/library/argparse.html#choices)
parser.add_argument('arg4', choices=['rock', 'paper', 'scissors'])
 
# Argumento opcional. Si se pametriza, requiere acompañarlo de un valor
parser.add_argument('-opt1')
 
# Un argumento opcional puede tener varios nombres
parser.add_argument('-opt2', '--option2')
 
# Argumento opcional con una descripción. Si se pametriza, requiere 
# acompañarlo de un valor de tipo int
parser.add_argument('-opt3', help='help for opt3', type=int)
 
# Argumento opcional con una descripción. Si se pametriza, requiere 
# acompañarlo de un valor de tipo int. Por defecto el valor es 10
parser.add_argument('-opt4', help='help for opt4', type=int, default=10)
 
# Argumento opcional. Con 'action' damos valor si el argumento se parametriza 
# (https://docs.python.org/2/library/argparse.html#action)
parser.add_argument('-opt5', '--option5', help='help for opt5', 
action='store_true', default=False)
 
# Argumento opcional requerido
parser.add_argument('-opt6', required=True)
 
# Argumento opcional con tres opciones posibles
# (https://docs.python.org/2/library/argparse.html#choices)
parser.add_argument('-opt7', choices=['rock', 'paper', 'scissors'])
 
# Argumento opcional que requiere dos argumentos
parser.add_argument('-opt8', nargs=2)
 
# Argumento opcional que requiere de 1 a N argumentos
parser.add_argument('-opt9', nargs='+')
 
# Argumento opcional que requiere de 0 a N argumentos
parser.add_argument('-opt10', nargs='*')
 
# Por último parsear los argumentos
args = parser.parse_args()
 
# Imprimir los parametros
print('args.arg2:', args.arg2)
print('args.arg1:', args.arg1)
print('args.arg3:', args.arg3)
print('args.arg2:', args.arg4)
print('args.opt1:', args.opt1)
print('args.opt2:', args.option2)
print('args.opt3:', args.opt3)
print('args.opt4:', args.opt4)
print('args.opt5:', args.option5)
print('args.opt6:', args.opt6)
print('args.opt7:', args.opt7)
print('args.opt8:', args.opt8)
print('args.opt9:', args.opt9)
print('args.opt10:', args.opt10)