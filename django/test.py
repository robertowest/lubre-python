import django
import csv

from contactos.models import Contacto, Empresa


def busqueda():
    e=Empresa.objects.get(id=1)
    print(e.contacto_empresas.all())
    
    c=Contacto.objects.get(id=1)
    print(c.empresas.all())


def crear_empresa(reg):
    emp = Empresa.objects.create()
    emp.nombre = reg['Razon Social']
    emp.razon_social = reg['Razon Social']
    emp.cuit = reg['CUIT']
    emp.telefono1 = reg['Tel1']
    emp.telefono2 = reg['Tel2']
    emp.vendedor = reg['Vendedor']
    emp.actividad = reg['Actividad']
    emp.id_referencia = reg['idGest']
    emp.save()
    return emp


def crear_contacto(reg):
    if Contacto.objects.filter(numero_tel=reg['Movil']).exists():
        con = Contacto.objects.get(numero_tel=reg['Movil'])
    else:
        con = Contacto.objects.create()
        con.nombre = reg['Nombre']
        con.apellido = reg['Apellido']
        con.tipo_tel = 'movil'
        con.area_tel = ''
        con.numero_tel = reg['Movil']
        con.email = reg['Correo']
        con.save()
    return con


def asociar_contacto():
    pass


def leer_csv():
    with open('Contactos.csv') as csvarchivo:
        entrada = csv.DictReader(csvarchivo, delimiter=';', quoting=csv.QUOTE_NONE)
        for (contador, reg) in enumerate(entrada):
            try:
                emp = crear_empresa(reg)
                con = crear_contacto(reg)
                con.empresas = emp
                con.save()

            except BaseException:
                print('Error al procesar linea número ', contador + 2)
                raise


leer_csv()
