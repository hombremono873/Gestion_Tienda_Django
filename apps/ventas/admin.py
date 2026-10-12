from django.contrib import admin
from .models import Consecutivo, Venta, DetalleVenta, Factura

# Register your models here.
admin.site.register(Consecutivo)
admin.site.register(Venta)
admin.site.register(DetalleVenta)
admin.site.register(Factura)
