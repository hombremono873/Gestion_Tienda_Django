from django.conf import settings
from django.db import models
from django.db.models import Q

from apps.core.constantes import MotivosMovimiento, TiposMovimiento

# Create your models here.

"""
MovimientoInventario (kárdex): cada cambio de stock deja un movimiento.
- Stock y movimiento cambian siempre juntos, dentro de la misma transacción.
- Tipo y motivo deben coincidir con el documento de origen:
    VENTA     -> SALIDA,  con venta,  sin compra
    COMPRA    -> ENTRADA, con compra, sin venta
    ANULACION -> ENTRADA, con venta,  sin compra (devuelve lo vendido)
    AJUSTE    -> ENTRADA o SALIDA, sin venta ni compra (solo ADMIN)
- FKs con texto hacia ventas y proveedores para evitar importaciones circulares.
"""
class MovimientoInventario(models.Model):
    producto = models.ForeignKey("productos.Producto", on_delete=models.PROTECT, related_name="movimientos")
    tipo = models.CharField("Tipo", max_length=10, choices=TiposMovimiento.choices)
    cantidad = models.PositiveIntegerField("Cantidad")
    motivo = models.CharField("Motivo", max_length=20, choices=MotivosMovimiento.choices)
    observacion = models.CharField("Observación", max_length=200, blank=True)
    venta = models.ForeignKey("ventas.Venta", on_delete=models.PROTECT, null=True, blank=True, related_name="movimientos")
    compra = models.ForeignKey("proveedores.Compra", on_delete=models.PROTECT, null=True, blank=True, related_name="movimientos")
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="movimientos_inventario")
    fecha = models.DateTimeField("Fecha", auto_now_add=True, db_index=True)

    class Meta:
        db_table = "movimientos_inventario"
        verbose_name = "Movimiento de inventario"
        verbose_name_plural = "Movimientos de inventario"
        ordering = ["-fecha"]
        indexes = [
            models.Index(fields=["producto", "fecha"], name="movimientos_producto_fecha"),
        ]

        constraints = [
            models.CheckConstraint(
                condition=Q(cantidad__gt=0),
                name="movimientos_inventario_cantidad_positiva",
                violation_error_message="La cantidad debe ser mayor que cero"
            ),
            models.CheckConstraint(
                condition=Q(tipo__in=TiposMovimiento.values),
                name="movimientos_inventario_tipo_valido",
                violation_error_message="El tipo de movimiento no es válido"
            ),
            models.CheckConstraint(
                condition=Q(motivo__in=MotivosMovimiento.values),
                name="movimientos_inventario_motivo_valido",
                violation_error_message="El motivo del movimiento no es válido"
            ),
            models.CheckConstraint(
                condition=Q(motivo=MotivosMovimiento.VENTA, tipo=TiposMovimiento.SALIDA,
                            venta__isnull=False, compra__isnull=True)
                        | Q(motivo=MotivosMovimiento.COMPRA, tipo=TiposMovimiento.ENTRADA,
                            compra__isnull=False, venta__isnull=True)
                        | Q(motivo=MotivosMovimiento.ANULACION, tipo=TiposMovimiento.ENTRADA,
                            venta__isnull=False, compra__isnull=True)
                        | Q(motivo=MotivosMovimiento.AJUSTE, venta__isnull=True, compra__isnull=True),
                name="movimientos_inventario_origen_coherente",
                violation_error_message="El tipo y el documento de origen no corresponden al motivo"
            ),
        ]

    def __str__(self):
        return f"{self.get_tipo_display()} {self.cantidad} - {self.producto} ({self.get_motivo_display()})"
