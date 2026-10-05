from django.contrib import admin
from .models import Cargo, Empleado, PagoSalario

# Register your models here.
admin.site.register(Cargo)
admin.site.register(Empleado)
admin.site.register(PagoSalario)