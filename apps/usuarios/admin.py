from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.empleados.models import Cargo

from .models import Usuario

"""Registro del modelo Cargo """
admin.site.register(Cargo)

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """Admin de usuarios adaptado al login por correo (el modelo no tiene username)."""

    ordering = ['email']
    list_display = ['email', 'first_name', 'last_name', 'rol', 'is_active']
    list_filter = ['rol', 'is_active']
    search_fields = ['email', 'first_name', 'last_name', 'documento']
    fieldsets = [
        (None, {'fields': ['email', 'password']}),
        ('Datos personales', {'fields': ['first_name', 'last_name', 'tipo_documento', 'documento', 'telefono']}),
        ('Rol y permisos', {'fields': ['rol', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions']}),
        ('Fechas', {'fields': ['last_login', 'date_joined']}),
    ]
    add_fieldsets = [
        (None, {'classes': ['wide'], 'fields': ['email', 'first_name', 'last_name', 'tipo_documento',
                                                'documento', 'rol', 'password1', 'password2']}),
    ]
