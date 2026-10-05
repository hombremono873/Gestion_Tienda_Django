from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
# Create your models here.

CHOICES = (
    ("CC", "CC"),
    ("CE", "CE"),
    ("TI", "TI"),
    ("NIT", "NIT"),
    ("PP", "PP")
)
class Cliente(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    nombre = models.CharField("Nombre del cliente", max_length=150)
    tipo_documento = models.CharField("Tipo de documento", max_length=3, choices=CHOICES, default = "CC")
    numero_documento = models.CharField("Número de documento", max_length=20,
                                        validators=[RegexValidator(r'^\d+$', 'Solo dígitos.')])
    telefono = models.CharField("Teléfono del cliente", max_length=20, blank=True)
    correo = models.EmailField("Correo del cliente", max_length=100, blank=True)
    direccion = models.CharField("Dirección del cliente", max_length=200, blank=True)
    fecha_registro = models.DateTimeField("Fecha de registro", auto_now_add=True)

    class Meta:
        db_table = "clientes"
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        constraints = [
            models.UniqueConstraint(
                fields=["tipo_documento", "numero_documento"],
                name="clientes_documento_unico",
                violation_error_message="Ya existe un cliente con ese tipo y número de documento"
            ),
            models.CheckConstraint(
                condition=models.Q(tipo_documento__in=["CC", "CE", "TI", "NIT", "PP"]),
                name="clientes_tipo_documento_valido",
                violation_error_message="El tipo de documento no es válido"
            ),
        ]
    def __str__(self):
        return self.nombre    