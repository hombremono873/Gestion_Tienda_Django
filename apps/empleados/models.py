from django.db import models
from django.conf import settings
from apps.usuarios.models import Usuario
# Create your models here.

"""Modelo para representar los cargos de los empleados"""
class Cargo(models.Model):
      nombre = models.CharField("Nombre del cargo", max_length=100, unique=True)
      descripcion = models.TextField("Descripción del cargo", blank=False)

      def __str__(self):
            return self.nombre
      
"""
Definición: Regla de integridad referencial para el parámetro
on_delete en relaciones de Django.
Comportamiento: Impide eliminar un registro principal (padre)
si existen registros dependientes (hijos) asociados a él.
Propósito: Evitar inconsistencias y registros huérfanos en la base de datos;
lanza un error si se intenta borrar un elemento que aún tiene dependencias activas.

RESTRICT: util para mantener la integridad referencial, evita borrar relaciones críticas
 """
OPCIONES = [
    ("Activo", "Activo"),
    ("Inactivo", "Inactivo"),
    ("Vacaciones", "Vacaciones"),
    ("Licencia", "Licencia"),
    ("Permiso", "Permiso"),
    ("Retirado", "Retirado"),
    ("Suspendido", "Suspendido")
]
class Empleado(models.Model):
      usuario = models.OneToOneField(
                settings.AUTH_USER_MODEL
                , on_delete=models.RESTRICT)
      cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT)  
      fecha_ingreso = models.DateField(
            "Fecha de ingreso",
             auto_now_add=True)
      #Validar CHCK >=0
      salario = models.DecimalField(
            "Salario",
             max_digits=10,
             decimal_places=2)
      #Validad CHECK = ACTIVO
      estado = models.CharField(
            "Estado del empleado",
             max_length=10,
             choices = OPCIONES,
             default = "ACTIVO")
      
      class Meta:
             pass 
       
      