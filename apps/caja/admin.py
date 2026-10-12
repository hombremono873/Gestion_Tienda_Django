from django.contrib import admin
from .models import Caja, SesionCaja, Pago
# Register your models here.
admin.site.register(Caja)
admin.site.register(SesionCaja)
admin.site.register(Pago)