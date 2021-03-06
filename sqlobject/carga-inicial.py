#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import sys

from sqlobject import *

# sqlhub.processConnection = connectionForURI('sqlite:/:memory:')
sqlhub.processConnection = connectionForURI('sqlite:contactos.sqlite3')


class Empresa(SQLObject):
    cuit = StringCol(length=13, unique=True)
    nombre = StringCol(length=60, notNone=True)
    razon_social = StringCol(length=60)
    telefono1 = StringCol(length=13)
    telefono2 = StringCol(length=13)
    vendedor = StringCol(length=30)
    actividad = StringCol(length=30)
    id_referencia = IntCol(unique=True)
    contacto = RelatedJoin('Contacto')

        
class Contacto(SQLObject):
    nombre = StringCol(length=30)
    apellido = StringCol(length=30)
    telefono = StringCol(length=15, notNone=True, unique=True)
    email = StringCol(length=60, unique=True)
    empresa = RelatedJoin('Empresa')


"""
class InsertarDatos():
    e = Empresa(cuit='20-20203910-', nombre='Roberto West SA', 
                razon_social='SERVER Consultorio Informático',
                telefono1='0381-4252884', telefono2='',
                vendedor='ninguno',
                actividad='ninguna',
                id_referencia=0
    )
    
    c = Contacto(nombre='Roberto', apellido='West',
                 telefono='0381-616-8251',
                 email='roberto@correo.com'
    )
    
    e.addContacto(c)
"""

class LeerDatos():
    with open('Contactos.csv') as csvarchivo:
        entrada = csv.DictReader(csvarchivo, delimiter=';', quoting=csv.QUOTE_NONE)
        for reg in entrada:
            try:
                print('Empresa: ', reg['Razon Social'])

                e = Empresa(cuit=reg['CUIT'], nombre=reg['Razon Social'], 
                            razon_social=reg['Razon Social'],
                            telefono1=reg['Tel1'], telefono2=reg['Tel2'],
                            vendedor=reg['Vendedor'],
                            actividad=reg['Actividad'],
                            id_referencia=int(reg['idGest'])
                )
                                
                c = Contacto(nombre=reg['Nombre'], apellido=reg['Apellido'],
                            telefono=reg['Movil'],
                            email=reg['Correo']
                )
                
                e.addContacto(c)

            except:
                print("Error inesperado:", sys.exc_info()[0])

"""
SQLObject.Error
SQLObject.DatabaseError
SQLObject.DataError
SQLObject.IntegrityError
SQLObject.DuplicateEntryError
SQLObject.InternalError
SQLObject.NotSupportedError
SQLObject.OperationalError
SQLObject.ProgrammingError
SQLObject.InterfaceError
SQLObject.Warning
"""

# Empresa.createTable()
# Contacto.createTable()

LeerDatos()
