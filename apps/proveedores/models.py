from django.core.validators import RegexValidator
from django.db import models
from apps.core.constantes import EstadosCompra
from django.utils import timezone
from django.conf import settings

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
     
class Compra(models.Model):
    proveedor = models.ForeignKey(Proveedor, models.PROTECT, related_name="compras") 
    numero_factura_proveedor = models.CharField("Número de factura del proveedor",max_length=30)
    fecha_compra = models.DateField("Fecha de compra",default=timezone.localdate)
    total  = models.DecimalField("Total de la compra",max_digits=12, decimal_places=2, default=0)
    estado = models.CharField("Estado de la compra", max_length=10, default=EstadosCompra.PENDIENTE, choices=EstadosCompra.choices)
    registrada_por =models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="compras_registradas")

    class Meta:
        db_table = "compras"
        verbose_name="Compra"
        verbose_name_plural = "Compras"
        
        constraints = [
               models.UniqueConstraint(
                   fields=["proveedor", "numero_factura_proveedor"],
                   name="compra_factura_proveedor_unica",
                   violation_error_message="Esta factura del proveedor ya está registrada"
                ),
               models.CheckConstraint(
                   condition=models.Q(total__gte=0),
                   name="compras_total_no_negativo",
                   violation_error_message="El total no puede ser negativo"
                ),
               models.CheckConstraint(
                   condition=models.Q(estado__in=EstadosCompra.values),
                   name="compras_estado_valido",
                   violation_error_message="El estado de la compra no es válido"
                ),
        ]
    def __str__(self):
        return f"{self.numero_factura_proveedor} - {self.proveedor.razon_social}"
"""
  subtotal costo_unitario*cantidad, se calcula en automatico
  fecha_vencimiento es opcional, para productos que tienen fecha de vencimiento

"""
class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name="detalles")
    producto = models.ForeignKey("productos.Producto", on_delete=models.PROTECT, related_name="detalles_compra")
    cantidad = models.PositiveIntegerField()
    costo_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    subtotal=models.DecimalField(max_digits=12, decimal_places=2)
    fecha_vencimiento = models.DateField(null=True, blank=True)

    class Meta:
        db_table = "detalles_compra"
        verbose_name = "Detalle de compra"
        verbose_name_plural = "Detalles de compra"

        constraints=[
              models.UniqueConstraint(
                  fields=["compra", "producto"],  #Un producto aparece una sola vez en cada compra
                  name="detalles_compra_producto_unico",
                  violation_error_message="Este producto ya está en la compra; modifica la cantidad"
              ),
              models.CheckConstraint(
                  condition=models.Q(cantidad__gt=0),
                  name="detalles_compra_cantidad_positiva",
                  violation_error_message="La cantidad de productos debe ser positiva"
              ),
              models.CheckConstraint(
                  condition=models.Q(costo_unitario__gte=0),
                  name="detalles_compra_costo_no_negativo",
                  violation_error_message="El costo unitario no puede ser negativo"
              ),
              models.CheckConstraint(
                  condition=models.Q(subtotal=models.F("cantidad")*models.F("costo_unitario")),
                  name="detalles_compra_subtotal_correcto",
                  violation_error_message="El subtotal debe ser cantidad × costo unitario"
              )
        ]

    def __str__(self):
        return f"{self.compra} - {self.producto} x {self.cantidad}"

class PagoProveedor(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.PROTECT, related_name="pagos")
    monto = models.DecimalField("Monto",max_digits=12, decimal_places=2)
    fecha = models.DateTimeField("Fecha", default=timezone.now)
    sesion_caja = models.ForeignKey("caja.SesionCaja", on_delete=models.PROTECT, null=True, blank=True, related_name="pagos_proveedor")
    registrado_por=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="pagos_proveedor_registrado")

    class Meta:
        db_table="pagos_proveedor"
        verbose_name="Pago a proveedor"
        verbose_name_plural="Pagos a proveedor"

        constraints=[
            models.CheckConstraint(
                condition=models.Q(monto__gt=0),
                name="pagos_proveedor_monto_positivo",
                violation_error_message="El monto del pago debe ser positivo"
            )
        ]

    def __str__(self):
        return f"{self.compra} - ${self.monto}"
