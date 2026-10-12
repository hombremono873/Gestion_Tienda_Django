from django.conf import settings
from django.db import models
from django.utils import timezone
from apps.core.constantes import EstadosSesion

# Create your models here.
class Caja(models.Model):
    nombre = models.CharField("Caja", max_length=50, unique=True)
    ubicacion = models.CharField("Ubicacion", max_length=100, blank=True)
    activa = models.BooleanField(default=True)

    class Meta:
        db_table ="cajas"
        verbose_name = "Caja"
        verbose_name_plural = "Cajas"
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre}"    
"""
  monto_esperado lo calcula el sistema en auto al cierre de la caaja,
  monto_esperado =base-ventas-pagos a proveedores)
  monto_contado lo escribe el empleado al cierre de caja
  diferencia =monto_contado - monto_esperado, se calcula en automatico
"""
class SesionCaja(models.Model):
    caja = models.ForeignKey(Caja, related_name="sesion", on_delete=models.PROTECT)
    empleado = models.ForeignKey("empleados.Empleado", related_name="sesion_caja", on_delete=models.PROTECT)
    fecha_apertura = models.DateTimeField(default=timezone.now)
    monto_inicial = models.DecimalField(max_digits=12, decimal_places=2)
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    monto_esperado = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    monto_contado = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    diferencia = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    estado = models.CharField("Estado", max_length=10, choices=EstadosSesion, default="ABIERTA")

    class Meta:
        db_table = "sesiones_caja"
        verbose_name = "Sesión de caja"
        verbose_name_plural = "Sesiones de caja"

        constraints = [
            models.UniqueConstraint(
                fields=["caja"],
                condition=models.Q(estado="ABIERTA"),
                name="sesion_caja_en_turno_abierto",
                violation_error_message="Esta caja tiene una sesión abierta"
            ),
            models.UniqueConstraint(
                fields=["empleado"],
                condition=models.Q(estado=EstadosSesion.ABIERTA),
                name="sesiones_caja_empleado_un_turno_abierto",
                violation_error_message="El empleado ya tiene un turno abierto"
            ),
            models.CheckConstraint(
                condition=models.Q(estado__in=EstadosSesion.values),
                name="sesiones_caja_estado_valido",
                violation_error_message="El estado de apertura o cierre de la caja no es valido"
            ),
            models.CheckConstraint(
                condition=models.Q(monto_inicial__gte=0) &
                          (models.Q(monto_contado__isnull=True) | models.Q(monto_contado__gte=0)),
                name="sesiones_caja_no_negativos",
                violation_error_message="El monto inicial y el monto contado no pueden ser negativos"
            ),
            models.CheckConstraint(
                condition=models.Q(estado=EstadosSesion.ABIERTA, fecha_cierre__isnull=True)
                        | models.Q(estado=EstadosSesion.CERRADA, fecha_cierre__isnull=False, monto_contado__isnull=False),
                name="sesiones_caja_cierre_coherente",
                violation_error_message="Una sesión abierta no tiene cierre; una cerrada debe tener fecha de cierre y monto contado"
            ),
        ]

    def __str__(self):
        return f"{self.caja}" + f"{self.estado}"   

"""
Pago: uno por venta (1:1). Solo efectivo, sin campo metodo (D-06).
- La relación 1:1 se declara aquí; desde la venta se llega con venta.pago.
- numero_recibo con prefijo RC, lo asigna el servicio al cobrar (D-10).
- monto = total de la venta; cambio = monto_recibido - monto.
"""
class Pago(models.Model):
    venta = models.OneToOneField("ventas.Venta", on_delete=models.PROTECT, related_name="pago")
    sesion_caja = models.ForeignKey(SesionCaja, on_delete=models.PROTECT, related_name="pagos")
    numero_recibo = models.CharField("Número de recibo", max_length=12, unique=True)
    monto = models.DecimalField("Monto", max_digits=12, decimal_places=2)
    monto_recibido = models.DecimalField("Efectivo recibido", max_digits=12, decimal_places=2)
    cambio = models.DecimalField("Cambio", max_digits=12, decimal_places=2)
    recibido_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="pagos_recibidos")
    fecha = models.DateTimeField("Fecha", auto_now_add=True)

    class Meta:
        db_table = "pagos"
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"

        constraints = [
            models.CheckConstraint(
                condition=models.Q(monto__gt=0),
                name="pagos_monto_positivo",
                violation_error_message="El monto del pago debe ser positivo"
            ),
            models.CheckConstraint(
                condition=models.Q(monto_recibido__gte=models.F("monto")),
                name="pagos_efectivo_suficiente",
                violation_error_message="El efectivo recibido no cubre el total"
            ),
            models.CheckConstraint(
                condition=models.Q(cambio=models.F("monto_recibido") - models.F("monto")),
                name="pagos_cambio_correcto",
                violation_error_message="El cambio debe ser efectivo recibido - monto"
            ),
        ]

    def __str__(self):
        return f"{self.numero_recibo} - {self.venta}"