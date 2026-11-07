from django.views.generic import TemplateView

from apps.core.constantes import Rol
from apps.core.mixins import RolRequeridoMixins


class Inicio(TemplateView):
    """Página pública de inicio: bienvenida y datos de la tienda. No exige sesión."""
    template_name = "core/inicio.html"


class PanelAdminView(RolRequeridoMixins, TemplateView):
    """Panel del administrador. Exige sesión y rol ADMIN; otro rol recibe 403."""
    template_name = "core/panel_admin.html"
    roles_permitidos = [Rol.ADMIN]
    # (ícono de Bootstrap Icons, título, descripción) de cada módulo
    extra_context = {"modulos": [
        ("bi-people", "Usuarios", "Crear, editar y desactivar cuentas."),
        ("bi-box-seam", "Productos", "Catálogo, categorías y precios."),
        ("bi-clipboard-data", "Inventario", "Stock, movimientos y ajustes."),
        ("bi-truck", "Proveedores y compras", "Proveedores, compras y pagos."),
        ("bi-person-vcard", "Clientes", "Datos de los clientes."),
        ("bi-receipt", "Ventas y facturas", "Consultar y anular ventas."),
        ("bi-cash-stack", "Caja", "Turnos y arqueos de todas las cajas."),
        ("bi-person-badge", "Empleados y nómina", "Cargos, empleados y pagos."),
        ("bi-graph-up", "Reportes", "Ventas, utilidades e inventario."),
    ]}


class PanelEmpleadoView(RolRequeridoMixins, TemplateView):
    """Panel del empleado (caja y ventas). Exige sesión y rol EMPLEADO; otro rol recibe 403."""
    template_name = "core/panel_empleado.html"
    roles_permitidos = [Rol.EMPLEADO]
    # Sin costos ni acumulado de caja (RNF-10)
    extra_context = {"modulos": [
        ("bi-cash-coin", "Mi turno de caja", "Abrir, cobrar y cerrar tu turno."),
        ("bi-cart-plus", "Nueva venta", "Registrar una venta y cobrarla."),
        ("bi-receipt", "Mis ventas", "Consultar las ventas que registraste."),
        ("bi-person-vcard", "Clientes", "Crear y consultar clientes."),
        ("bi-box-seam", "Productos y stock", "Consultar productos y existencias."),
        ("bi-wallet2", "Mis pagos", "Consultar tus pagos de salario."),
    ]}


class PanelClienteView(RolRequeridoMixins, TemplateView):
    """Panel del cliente (sus datos y facturas). Exige sesión y rol CLIENTE; otro rol recibe 403."""
    template_name = "core/panel_cliente.html"
    roles_permitidos = [Rol.CLIENTE]
    extra_context = {"modulos": [
        ("bi-receipt", "Mis facturas", "Consultar e imprimir tus facturas."),
        ("bi-person-circle", "Mis datos", "Ver y actualizar tu perfil."),
        ("bi-shop", "Catálogo", "Ver los productos de la tienda."),
    ]}
