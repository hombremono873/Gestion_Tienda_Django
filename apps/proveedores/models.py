from django.core.validators import RegexValidator
from django.db import models

# Create your models here.

class Proveedor(models.Model):
    nit = models.CharField("NIT del proveedor", max_length = 20, unique=True,
                           validators=[RegexValidator(r'^\d+(-\d)?$', 'NIT inválido. Ejemplo: 900123456-7')])
    razon_social=models.CharField("Razón social del preveedor", max_length = 150)
    contacto=models.CharField("Nombre del contacto", max_length = 100, blank = True)
    telefono=models.CharField("Teléfono del proveedor", max_length = 20)
    direccion=models.CharField("Direccion del proveedor", max_length = 200, blank = True)
    activo=models.BooleanField("Proveedor activo", default = True)

    class Meta:
        db_table = "proveedores"
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ["razon_social"]

    def __str__(self):
        return self.razon_social    