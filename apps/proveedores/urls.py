from django.urls import path

from . import views

app_name = 'proveedores'

urlpatterns = [
    path("", views.ProveedorView.as_view(), name="proveedor_list"),
    path("nuevo/", views.ProveedorCreateView.as_view(), name="proveedor_create"),
    path("actualizar/<int:pk>/", views.ProveedorUpdateView.as_view(), name = "proveedor_update"),
    path("desactivar/<int:pk>/", views.ProveedorDeactivateView.as_view(), name = "proveedor_deactivate"),
]
