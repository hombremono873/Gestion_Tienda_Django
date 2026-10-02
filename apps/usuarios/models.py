from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator

# Create your models here.

CHOICES = (
    ('CC', 'Cédula de Ciudadanía'),
    ('TI', 'Tarjeta de Identidad'),
    ('NIT', 'Número de Identificación Tributaria'),
    ('PP', 'Pasaporte'),
    ('CE', 'Cédula de Extranjería')
)
ROLES = [
    ("ADMIN", "Administrador"),
    ("EMPLEADO", "Empleado"),
    ("CLIENTE", "Cliente"),
]

"""
Clase Meta del modelo Usuario (va dentro de la clase, al final).

Meta guarda opciones del modelo completo, no de un campo. No crea columnas.
- db_table: nombre de la tabla en PostgreSQL (Documento 4: nombres en plural).
  Sin esto Django la llamaría "usuarios_usuario".
- verbose_name / verbose_name_plural: nombre que se muestra en el admin.
- constraints: reglas que la base de datos hace cumplir aunque el código falle
  (última barrera, D-04). Se crean en PostgreSQL al hacer migrate.
    * UniqueConstraint: la PAREJA tipo + número no se repite
      (una CC 900123 y un NIT 900123 son documentos distintos).
    * CheckConstraint: la base rechaza un tipo de documento o un rol
      que no esté en la lista.
"""


class UsuarioManager(BaseUserManager):
    """Crea usuarios con el correo como identificador, porque el modelo no tiene username."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('El correo es obligatorio.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # guarda la contraseña cifrada
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('rol', 'ADMIN')  # el superusuario es ADMIN (Documento 1)
        return self._create_user(email, password, **extra_fields)


class Usuario(AbstractUser):
    username=None
    first_name = models.CharField("nombres",max_length=150)
    last_name=models.CharField("apellidos", max_length=150)
    telefono=models.CharField("telefono", max_length=20, blank=True)
    documento=models.CharField("documento", max_length=20,
                               validators=[RegexValidator(r'^\d+$', 'Solo dígitos.')])
    tipo_documento=models.CharField("tipo", max_length=3, choices=CHOICES, default="CC")
    rol = models.CharField("rol", max_length=10, choices=ROLES, default="CLIENTE")
    email=models.EmailField("correo", max_length=254, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'tipo_documento', 'documento']

    objects = UsuarioManager()

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'usuarios'
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'
        constraints = [
            models.UniqueConstraint(
                fields=['tipo_documento', 'documento'],
                name='usuarios_documento_unico',
            ),
            models.CheckConstraint(
                condition=models.Q(tipo_documento__in=['CC', 'CE', 'TI', 'NIT', 'PP']),
                name='usuarios_tipo_documento_valido',
            ),
            models.CheckConstraint(
                condition=models.Q(rol__in=['ADMIN', 'EMPLEADO', 'CLIENTE']),
                name='usuarios_rol_valido',
            ),
        ]
