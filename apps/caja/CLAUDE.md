# app caja
> Fuente: Documento 4 (BD) v1.0 + decisiones 2026-10-01. Al escribir models.py, el código pasa a ser la verdad: dejar aquí solo reglas no obvias.

## Caja — cajas (fase 2)
* nombre CharField(50) UK · ubicacion CharField(100) null · activa Bool.

## SesionCaja — sesiones_caja (fase 5)
* caja FK(Caja, PROTECT) · empleado FK(Empleado, PROTECT).
* fecha_apertura · monto_inicial CHECK ≥0 · fecha_cierre null.
* monto_esperado null · monto_contado null CHECK ≥0 · diferencia null (contado − esperado).
* estado CHECK ABIERTA/CERRADA.
* UNIQUE(caja) y UNIQUE(empleado) con condition estado='ABIERTA'.

## Pago — pagos (fase 7) — uno por venta
* venta OneToOne("ventas.Venta", PROTECT) · sesion_caja FK(SesionCaja, PROTECT).
* numero_recibo CharField(12) UK (prefijo RC) · monto CHECK >0 (= total venta).
* monto_recibido CHECK ≥ monto · cambio CHECK ≥0 · recibido_por FK(Usuario, PROTECT) · fecha auto_now_add.
* Sin campo metodo (D-06).

## Servicios
* abrir_turno(): atómico; IntegrityError por constraint → excepción propia (CU-03 4a).
* cerrar_turno(): lock turno. esperado = base + Σ pagos del turno − Σ pagos_proveedor del turno − Σ devoluciones de ventas anuladas con este turno (P1).
* No cerrar con carrito en curso. Cobro y cierre bloquean la fila del turno.

## Reglas
* Cierre a ciegas: el empleado no ve el esperado antes de contar (RN-13, RNF-10).
* EMPLEADO abre, cobra y cierra su turno. ADMIN ve todos (RF-21).

## Plantillas
apertura, pago_form, cierre, caja_historial.
