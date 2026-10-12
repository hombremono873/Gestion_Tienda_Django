from django.contrib import admin
from .models import Proveedor, Compra, DetalleCompra, PagoProveedor

# Register your models here.
admin.site.register(Proveedor)
admin.site.register(Compra)
admin.site.register(DetalleCompra)
admin.site.register(PagoProveedor)