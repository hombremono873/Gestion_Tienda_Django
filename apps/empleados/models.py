from django.conf import settings
from django.db import models
from django.utils import timezone


class Cargo(models.Model):
    """Puesto de trabajo con su salario de referencia."""

    nombre = models.CharField("Nombre del cargo", max_length=80, unique=True)
    salario_base = models.DecimalField("Salario base", max_digits=12, decimal_places=2)
    descripcion = models.TextField("Descripción del cargo", blank=True)

    class Meta:
        db_table = "cargos"
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(salario_base__gte=0),
                name="salario_base_cargo_no_negativo",
                violation_error_message="El salario base no puede ser negativo",
            ),
        ]

    def __str__(self):
        return self.nombre


"""
on_delete=PROTECT (Documento 4)
Definición: Regla de integridad referencial para el parámetro
on_delete en relaciones de Django.
Comportamiento: Impide eliminar un registro principal (padre)
si existen registros dependientes (hijos) asociados a él.
Propósito: Evitar inconsistencias y registros huérfanos en la base de datos;
lanza un error si se intenta borrar un elemento que aún tiene dependencias activas.
"""

ESTADOS = [
    ("ACTIVO", "Activo"),
    ("INACTIVO", "Inactivo"),
    ("VACACIONES", "Vacaciones"),
    ("LICENCIA", "Licencia"),
    ("PERMISO", "Permiso"),
    ("RETIRADO", "Retirado"),
    ("SUSPENDIDO", "Suspendido"),
]


class Empleado(models.Model):
    """Persona que trabaja en la tienda, enlazada a una cuenta de usuario."""

    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT)
   
    fecha_ingreso = models.DateField("Fecha de ingreso", default=timezone.localdate)
    salario = models.DecimalField("Salario", max_digits=12, decimal_places=2)
    estado = models.CharField(
        "Estado del empleado",
        max_length=15,
        choices=ESTADOS,
        default="ACTIVO",
    )

    class Meta:
        db_table = "empleados"
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(salario__gte=0),
                name="salario_empleado_no_negativo",
                violation_error_message="El salario no puede ser negativo",
            ),
            models.CheckConstraint(
                condition=models.Q(estado__in=[valor for valor, _ in ESTADOS]),
                name="estado_empleado_valido",
                violation_error_message="El estado del empleado no es válido",
            ),
        ]

    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.cargo.nombre}"
    
class  PagoSalario(models.Model): 
    empleado = models.ForeignKey(Empleado, on_delete=models.PROTECT)
    periodo_inicio = models.DateField("Periodo de inicio")
    periodo_fin = models.DateField("Periodo de fin")
    salario_base = models.DecimalField("Salario base", max_digits=12, decimal_places=2)
    bonificaciones = models.DecimalField("Bonificaciones", max_digits=12, decimal_places=2, default=0)
    deducciones = models.DecimalField("Deducciones", max_digits=12, decimal_places=2, default=0)
    total_pagado = models.DecimalField("Total a pagar", max_digits=12, decimal_places=2)
    fecha_pago = models.DateField("Fecha de pago", default=timezone.localdate)
    registrado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="pagos_salario_registrados_por")

    class Meta:
        db_table = "pagos_salarios"
        verbose_name = "Pago de salario"
        verbose_name_plural = "Pagos de salario"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(salario_base__gte=0),
                name="salario_base_no_negativo",
                violation_error_message="El salario base no puede ser negativo",
            ),
            models.CheckConstraint(
                condition=models.Q(bonificaciones__gte=0),
                name="bonificaciones_no_negativas",
                violation_error_message="Las bonificaciones no pueden ser negativas",
            ),
            models.CheckConstraint(
                condition=models.Q(deducciones__gte=0),
                name="deducciones_no_negativas",
                violation_error_message="Las deducciones no pueden ser negativas",
            ),
            models.CheckConstraint(
                condition=models.Q(total_pagado__gte=0),
                name="total_pago_no_negativo",
                violation_error_message="El total a pagar no puede ser negativo",
            ),
            models.UniqueConstraint(
                fields = ["empleado", "periodo_inicio", "periodo_fin"],
                name = "pago_unico_por_periodo",
                violation_error_message = "Ya existe un pago registrado para este empleado en el periodo especificado"
            ),
            models.CheckConstraint(
                condition=models.Q(periodo_fin__gte=models.F("periodo_inicio")),
                name="pagos_salario_periodo_valido",
                violation_error_message="La fecha final del periodo no puede ser anterior a la inicial",
            ),
            

        ]

    def __str__(self):
        return f"{self.empleado.usuario.get_full_name()} - {self.periodo_inicio} - {self.periodo_fin}"
