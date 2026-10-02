# app clientes
> Fuente: Documento 4 (BD) v1.0 + decisiones 2026-10-01. Al escribir models.py, el código pasa a ser la verdad: dejar aquí solo reglas no obvias.

## Cliente — clientes (fase 3)
* usuario OneToOne(Usuario, SET_NULL) null — vacío si lo registra un empleado.
* nombre CharField(150) · tipo_documento CHECK CC/CE/TI/NIT/PP · numero_documento CharField(20).
* telefono CharField(20) null · correo Email null · direccion CharField(200) null.
* fecha_registro DateTime auto_now_add.
* Constraint: UNIQUE(tipo_documento, numero_documento).

## Reglas
* Venta sin cliente = consumidor final.
* Empleado que compra → se registra aquí sin cuenta (P3).
* EMPLEADO crea y consulta (búsqueda por documento, RF-16); CLIENTE ve solo sus datos.

## Plantillas
cliente_lista, cliente_form, cliente_detalle.
