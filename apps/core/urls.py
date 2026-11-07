from django.urls import path

from .views import Inicio, PanelAdminView, PanelEmpleadoView, PanelClienteView

app_name = 'core'

urlpatterns = [
    path("", Inicio.as_view(), name="inicio"),
    path("panel/admin/", PanelAdminView.as_view(), name="panel_admin"),
    path("panel/empleado/", PanelEmpleadoView.as_view(), name="panel_empleado"),
    path("panel/cliente/", PanelClienteView.as_view(), name="panel_cliente"),
]
