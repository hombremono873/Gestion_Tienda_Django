"""
Constantes compartidas del proyecto (opciones de campos e impuestos).

Uso en un modelo:
    choices=TipoDocumento.choices, default=TipoDocumento.CC
    condition=models.Q(tipo_documento__in=TipoDocumento.values)
Cada valor se define una sola vez aquí; los CHECK de la BD leen .values.
"""

from django.db import models


class TipoDocumento(models.TextChoices):
    CC = "CC", "Cédula de Ciudadanía"
    TI = "TI", "Tarjeta de Identidad"
    NIT = "NIT", "Número de Identificación Tributaria"
    PP = "PP", "Pasaporte"
    CE = "CE", "Cédula de Extranjería"


class Rol(models.TextChoices):
    ADMIN = "ADMIN", "Administrador"
    EMPLEADO = "EMPLEADO", "Empleado"
    CLIENTE = "CLIENTE", "Cliente"


class EstadoEmpleado(models.TextChoices):
    ACTIVO = "ACTIVO", "Activo"
    INACTIVO = "INACTIVO", "Inactivo"
    VACACIONES = "VACACIONES", "Vacaciones"
    LICENCIA = "LICENCIA", "Licencia"
    PERMISO = "PERMISO", "Permiso"
    RETIRADO = "RETIRADO", "Retirado"
    SUSPENDIDO = "SUSPENDIDO", "Suspendido"


class TarifaIVA(models.IntegerChoices):
    """Tarifas de IVA en Colombia (%). El IVA se suma a precio_venta al vender."""

    CERO = 0, "0 %"
    CINCO = 5, "5 %"
    DIECINUEVE = 19, "19 %"


class ClasificacionIVA(models.TextChoices):
    GRAVADO = "GRAVADO", "Gravado"
    EXENTO = "EXENTO", "Exento"
    EXCLUIDO = "EXCLUIDO", "Excluido"

class EstadosCompra(models.TextChoices):
    PENDIENTE = "PENDIENTE", "Pendiente"
    PAGADA = "PAGADA", "Pagada"  
    ANULADA = "ANULADA", "Anulada"  

class EstadosSesion(models.TextChoices):
    ABIERTA = "ABIERTA", "Abierta"
    CERRADA = "CERRADA", "Cerrada"


class EstadosVenta(models.TextChoices):
    """La venta nace PAGADA al cobrar (D-07); no existe PENDIENTE."""

    PAGADA = "PAGADA", "Pagada"
    ANULADA = "ANULADA", "Anulada"


class EstadosFactura(models.TextChoices):
    VIGENTE = "VIGENTE", "Vigente"
    ANULADA = "ANULADA", "Anulada"


class TiposMovimiento(models.TextChoices):
    ENTRADA = "ENTRADA", "Entrada"
    SALIDA = "SALIDA", "Salida"


class MotivosMovimiento(models.TextChoices):
    VENTA = "VENTA", "Venta"
    COMPRA = "COMPRA", "Compra"
    AJUSTE = "AJUSTE", "Ajuste"
    ANULACION = "ANULACION", "Anulación de venta"
    