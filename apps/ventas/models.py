from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.core.constantes import EstadosFactura, EstadosVenta, TarifaIVA

# Create your models here.

"""
Consecutivo (D-10): numeración sin huecos ni repetidos para V, FV y RC.
- El servicio siguiente_numero(prefijo) bloquea la fila con select_for_update()
  y suma 1, dentro de la transacción del cobro.
- Las filas V, FV y RC se crean en 0 con una migración de datos.
"""
class Consecutivo(models.Model):
    prefijo = models.CharField("Prefijo", max_length=5, unique=True)
    descripcion = models.CharField("Descripción", max_length=50)
    ultimo_numero = models.PositiveIntegerField("Último número", default=0)

    class Meta:
        db_table = "consecutivos"
        verbose_name = "Consecutivo"
        verbose_name_plural = "Consecutivos"
        ordering = ["prefijo"]

        constraints = [
            models.CheckConstraint(
                condition=models.Q(ultimo_numero__gte=0),
                name="consecutivos_numero_no_negativo",
                violation_error_message="El último número no puede ser negativo"
            ),
        ]

    def __str__(self):
        return f"{self.prefijo} - {self.ultimo_numero}"


"""
Venta: se guarda SOLO al cobrar y nace PAGADA (D-07).
- cliente nulo = consumidor final.
- total = subtotal - descuento + iva (el IVA se suma a precio_venta, CP-31).
- Al anular (solo ADMIN, P1): se devuelve el efectivo desde un turno ABIERTO
  que el ADMIN elige -> sesion_caja_devolucion. Resta en el arqueo de ese turno.
- Dos FK a SesionCaja: cada una necesita su related_name.
"""
class Venta(models.Model):
    numero_venta = models.CharField("Número de venta", max_length=12, unique=True)
    cliente = models.ForeignKey("clientes.Cliente", on_delete=models.PROTECT, null=True, blank=True, related_name="ventas")
    empleado = models.ForeignKey("empleados.Empleado", on_delete=models.PROTECT, related_name="ventas")
    sesion_caja = models.ForeignKey("caja.SesionCaja", on_delete=models.PROTECT, related_name="ventas")
    fecha = models.DateTimeField("Fecha", default=timezone.now, db_index=True)
    subtotal = models.DecimalField("Subtotal", max_digits=12, decimal_places=2)
    descuento = models.DecimalField("Descuento", max_digits=12, decimal_places=2, default=0)
    iva = models.DecimalField("IVA", max_digits=12, decimal_places=2)
    total = models.DecimalField("Total", max_digits=12, decimal_places=2)
    estado = models.CharField("Estado", max_length=10, choices=EstadosVenta.choices, default=EstadosVenta.PAGADA, db_index=True)
    motivo_anulacion = models.CharField("Motivo de anulación", max_length=200, blank=True)
    fecha_anulacion = models.DateTimeField("Fecha de anulación", null=True, blank=True)
    anulada_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name="ventas_anuladas")
    sesion_caja_devolucion = models.ForeignKey("caja.SesionCaja", on_delete=models.PROTECT, null=True, blank=True, related_name="devoluciones")

    class Meta:
        db_table = "ventas"
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        ordering = ["-fecha"]

        constraints = [
            models.CheckConstraint(
                condition=models.Q(subtotal__gte=0, iva__gte=0, total__gte=0),
                name="ventas_montos_no_negativos",
                violation_error_message="Subtotal, IVA y total no pueden ser negativos"
            ),
            models.CheckConstraint(
                condition=models.Q(descuento__gte=0, descuento__lte=models.F("subtotal")),
                name="ventas_descuento_valido",
                violation_error_message="El descuento no puede ser negativo ni mayor que el subtotal"
            ),
            models.CheckConstraint(
                condition=models.Q(total=models.F("subtotal") - models.F("descuento") + models.F("iva")),
                name="ventas_total_correcto",
                violation_error_message="El total debe ser subtotal - descuento + IVA"
            ),
            models.CheckConstraint(
                condition=models.Q(estado__in=EstadosVenta.values),
                name="ventas_estado_valido",
                violation_error_message="El estado de la venta no es válido"
            ),
            models.CheckConstraint(
                condition=models.Q(estado=EstadosVenta.PAGADA, fecha_anulacion__isnull=True,
                                   anulada_por__isnull=True, sesion_caja_devolucion__isnull=True)
                        | models.Q(estado=EstadosVenta.ANULADA, fecha_anulacion__isnull=False,
                                   anulada_por__isnull=False, sesion_caja_devolucion__isnull=False),
                name="ventas_anulacion_coherente",
                violation_error_message="Una venta anulada debe tener fecha, responsable y turno de devolución; una pagada no"
            ),
        ]

    def __str__(self):
        return f"{self.numero_venta} - ${self.total}"

"""
DetalleVenta: una línea por producto en la venta.
- precio_unitario y porcentaje_iva se COPIAN del producto al cobrar (RN-09):
  si el precio cambia después, la venta conserva lo que se cobró.
- subtotal = cantidad * precio_unitario (sin IVA).
"""
class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name="detalles")
    producto = models.ForeignKey("productos.Producto", on_delete=models.PROTECT, related_name="detalles_venta")
    cantidad = models.PositiveIntegerField("Cantidad")
    precio_unitario = models.DecimalField("Precio unitario", max_digits=12, decimal_places=2)
    porcentaje_iva = models.DecimalField("Porcentaje de IVA", max_digits=5, decimal_places=2, choices=TarifaIVA.choices)
    subtotal = models.DecimalField("Subtotal", max_digits=12, decimal_places=2)

    class Meta:
        db_table = "detalles_venta"
        verbose_name = "Detalle de venta"
        verbose_name_plural = "Detalles de venta"

        constraints = [
            models.UniqueConstraint(
                fields=["venta", "producto"],
                name="detalles_venta_producto_unico",
                violation_error_message="Este producto ya está en la venta; modifica la cantidad"
            ),
            models.CheckConstraint(
                condition=models.Q(cantidad__gt=0),
                name="detalles_venta_cantidad_positiva",
                violation_error_message="La cantidad debe ser mayor que cero"
            ),
            models.CheckConstraint(
                condition=models.Q(precio_unitario__gte=0),
                name="detalles_venta_precio_no_negativo",
                violation_error_message="El precio unitario no puede ser negativo"
            ),
            models.CheckConstraint(
                condition=models.Q(porcentaje_iva__in=TarifaIVA.values),
                name="detalles_venta_iva_valido",
                violation_error_message="El porcentaje de IVA debe ser 0, 5 o 19"
            ),
            models.CheckConstraint(
                condition=models.Q(subtotal=models.F("cantidad") * models.F("precio_unitario")),
                name="detalles_venta_subtotal_correcto",
                violation_error_message="El subtotal debe ser cantidad × precio unitario"
            ),
        ]

    def __str__(self):
        return f"{self.venta} - {self.producto} x {self.cantidad}"


"""
Factura: interna e imprimible (sin DIAN). Una por venta (1:1, venta.factura).
- prefijo FV + numero desde Consecutivo, asignados al cobrar (D-10).
- Al anular la venta, la factura pasa a ANULADA; nunca se borra (RN-16).
"""
class Factura(models.Model):
    venta = models.OneToOneField(Venta, on_delete=models.PROTECT, related_name="factura")
    prefijo = models.CharField("Prefijo", max_length=5, default="FV")
    numero = models.PositiveIntegerField("Número")
    fecha_emision = models.DateTimeField("Fecha de emisión", default=timezone.now)
    total = models.DecimalField("Total", max_digits=12, decimal_places=2)
    estado = models.CharField("Estado", max_length=10, choices=EstadosFactura.choices, default=EstadosFactura.VIGENTE)

    class Meta:
        db_table = "facturas"
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"
        ordering = ["-fecha_emision"]

        constraints = [
            models.UniqueConstraint(
                fields=["prefijo", "numero"],
                name="facturas_numero_unico",
                violation_error_message="Ya existe una factura con ese número"
            ),
            models.CheckConstraint(
                condition=models.Q(total__gte=0),
                name="facturas_total_no_negativo",
                violation_error_message="El total no puede ser negativo"
            ),
            models.CheckConstraint(
                condition=models.Q(estado__in=EstadosFactura.values),
                name="facturas_estado_valido",
                violation_error_message="El estado de la factura no es válido"
            ),
        ]

    def __str__(self):
        return f"{self.prefijo}-{self.numero:06d}"
