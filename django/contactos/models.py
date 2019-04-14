from django.urls import reverse
from django.db import models

class Empresa(models.Model):
    cuit = models.CharField(max_length=13, null=True, blank=True, unique=True)
    nombre = models.CharField(max_length=60, null=True, blank=True)
    razon_social = models.CharField("Razón Social", max_length=60, null=True, blank=True)
    telefono1 = models.CharField("Teléfono 1", max_length=13, null=True, blank=True)
    telefono2 = models.CharField("Teléfono 2", max_length=13, null=True, blank=True)
    vendedor = models.CharField(max_length=30, null=True, blank=True)
    actividad = models.CharField(max_length=30, null=True, blank=True)
    id_referencia = models.IntegerField('Código Sistema de Gestión', null=True, unique=True)

    def __str__(self):
        return "%s" % (self.razon_social)

    def get_absolute_url(self):
        return reverse('empresa:empresa_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('empresa:empresa_update', args=(self.pk,))


TIPO_TEL = (('movil', 'Celular'), ('work', 'Trabajo'), ('home', 'Casa'), ('other', 'Otro'))


class Contacto(models.Model):
    nombre = models.CharField(max_length=30, null=True, blank=True)
    apellido = models.CharField(max_length=30, null=True, blank=True)
    tipo_tel = models.CharField('Tipo Teléfono', null=True, blank=True, max_length=5, choices=TIPO_TEL)
    area_tel = models.CharField('Area Teléfono', max_length=5, null=True, blank=True)
    numero_tel = models.CharField('Nro. Teléfono', max_length=15, null=True, blank=True, unique=True)
    email = models.EmailField("Correo Electrónico", max_length=150, null=True, blank=True, unique=True)
    empresas = models.ManyToManyField(Empresa, related_name='contacto_empresas', blank=True)

    def __str__(self):
        return "%s, %s" % (self.apellido, self.nombre)

    def get_absolute_url(self):
        return reverse('empresa:contacto_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('empresa:contacto_update', args=(self.pk,))
