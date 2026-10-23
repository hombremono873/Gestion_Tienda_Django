from django.db import transaction
from apps.clientes.models import Cliente
from .models import Usuario
from apps.core.constantes import Rol

class VinculoError(Exception):
     """Error de negocio al vincular un cliente con una cuenta."""


"""
Cliente.objects consulta la tabla clientes. .select_for_update() 
lee la fila y la bloquea hasta que termine la transacción, 
para que nadie más la modifique mientras tanto. .filter(tipo_documento=..., documento=...) 
busca el cliente con ese tipo y número de documento. Y .first() 
devuelve el primero que encuentre, o None si no existe, sin lanzar error
"""

def crear_cuenta(datos, rol):
    """Crea una cuenta de acceso. No sabe nada de clientes ni empleados."""
    usuario = Usuario.objects.create_user(
        email=datos["email"],
        password=datos["password1"],
        first_name=datos["first_name"],
        last_name=datos["last_name"],
        tipo_documento=datos["tipo_documento"],
        documento=datos["documento"],
        telefono=datos.get("telefono", ""), # tecnica recomendada para datos no obligatorios
        rol=rol,
    )
    return usuario

def registrar_cliente(datos):
    cliente = Cliente.objects.create(
        nombre = f"{datos["first_name"]} {datos["last_name"]}",
        tipo_documento = datos["tipo_documento"],
        numero_documento = datos["documento"],
        telefono = datos.get("telefono", ""),
        direccion=datos.get("direccion", ""),
        correo=datos.get("email", ""),
    )
    return cliente

def obtener_o_crear_cliente(datos):
    """Devuelve el cliente con ese documento (bloqueado); si no existe, lo crea.
       Cubre a quien ya compró sin cuenta (P3): se reutiliza su registro.
    """
    cliente = Cliente.objects.select_for_update().filter(
        tipo_documento=datos["tipo_documento"],
        numero_documento=datos["documento"],
    ).first()
    if cliente:
        return cliente
    return registrar_cliente(datos)
"""
   if cliente.usuario: valida que el cliente tenga un usuario
   si no se entra por el if se vincula el cliente con el usuario
   Al vincularlos, la app puede saber qué cliente es la persona que inició sesión y mostrarle sus datos:
"""
def vincular_cliente_cuenta(cliente, usuario):

    if cliente.usuario:
        raise VinculoError("El cliente ya tiene cuenta")
    
    cliente.usuario = usuario
    cliente.save(update_fields=["usuario"])
    return usuario

@transaction.atomic
def registrarse(datos):
    """Proceso de la página de registro: cuenta + cliente + vínculo, todo o nada."""
    usuario = crear_cuenta(datos, rol=Rol.CLIENTE)
    cliente = obtener_o_crear_cliente(datos)
    vincular_cliente_cuenta(cliente, usuario)
    return usuario
