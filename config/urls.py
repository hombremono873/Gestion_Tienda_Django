"""URLs principales de Gestiontienda. Cada app define sus rutas en su propio urls.py."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('usuarios/', include('apps.usuarios.urls')),
    path('clientes/', include('apps.clientes.urls')),
    path('empleados/', include('apps.empleados.urls')),
    path('productos/', include('apps.productos.urls')),
    path('inventario/', include('apps.inventario.urls')),
    path('proveedores/', include('apps.proveedores.urls')),
    path('ventas/', include('apps.ventas.urls')),
    path('caja/', include('apps.caja.urls')),
    path('reportes/', include('apps.reportes.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
