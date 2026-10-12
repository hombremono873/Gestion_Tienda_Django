from django.db import models

from apps.core.constantes import ClasificacionIVA, TarifaIVA

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField("Nombre de la categoría", max_length=100, unique=True)
    descripcion = models.TextField("Descripción de la categoria", blank = True)

    class Meta:
        db_table = "categorias"
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    codigo = models.CharField("Código del producto", max_length=30, unique=True)  
    nombre = models.CharField("Nombre del producto", max_length = 150, unique = True)  
    descripcion = models.TextField("Descripción del producto", blank = True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name="productos")
    proveedor = models.ForeignKey("proveedores.Proveedor", on_delete=models.SET_NULL, null = True, blank = True, related_name = "productos")
    precio_compra = models.DecimalField("Precio de compra", max_digits = 12, decimal_places = 2)
    porcentaje_iva = models.DecimalField("Porcentaje de IVA", max_digits = 5, decimal_places = 2, choices = TarifaIVA.choices)
    clasificacion_iva = models.CharField("Clasificación de IVA", max_length = 10, choices = ClasificacionIVA.choices)
    precio_venta = models.DecimalField("Precio de venta (sin IVA)", max_digits=12, decimal_places=2)
    stock = models.PositiveIntegerField("Stock disponible", default = 0)
    imagen = models.ImageField("Imagen del producto", upload_to="productos/", null=True, blank=True)
    activo = models.BooleanField("Activo", default = True)

    class Meta:
        db_table = "productos"
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        
        constraints = [
            models.CheckConstraint(
                condition=models.Q(precio_compra__gte=0),
                name="precio_compra_producto_no_negativo",
                violation_error_message="El precio de compra no puede ser negativo"
            ),
            models.CheckConstraint(
                condition = models.Q(precio_venta__gte=0),
                name = "precio_venta_producto_no_negativo",
                violation_error_message = "El precio de venta no puede ser negativo"
            ),
            models.CheckConstraint(
                condition=models.Q(porcentaje_iva__in=TarifaIVA.values),
                name="porcentaje_iva_producto_valido",
                violation_error_message="El porcentaje de IVA debe ser uno de los valores válidos"
            )
        ]
    def __str__(self):
        return f"{self.nombre} - {self.codigo}"    