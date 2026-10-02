# app proveedores
> Fuente: Documento 4 (BD) v1.0 + decisiones 2026-10-01. Al escribir models.py, el código pasa a ser la verdad: dejar aquí solo reglas no obvias.

## Proveedor — proveedores (fase 2)
* nit CharField(20) UK · razon_social CharField(150) · contacto CharField(100) null.
* telefono CharField(20) · correo Email null · direccion CharField(200) null · activo Bool.

## Compra — compras (fase 6)
* proveedor FK(Proveedor, PROTECT) · numero_factura_proveedor CharField(30) · fecha Date.
* total Dec CHECK ≥0 (Σ detalles) · estado CHECK PENDIENTE/PAGADA/ANULADA · registrado_por FK(Usuario, PROTECT).
* UNIQUE(proveedor, numero_factura_proveedor).

## DetalleCompra — detalles_compra
* compra FK(Compra, CASCADE) · producto FK(Producto, PROTECT) · cantidad PositiveInt CHECK >0.
* costo_unitario Dec CHECK ≥0 · subtotal = cantidad × costo_unitario. UNIQUE(compra, producto).

## PagoProveedor — pagos_proveedor
* compra FK(Compra, PROTECT) (abonos) · monto Dec CHECK >0 · fecha DateTime.
* sesion_caja FK("caja.SesionCaja", PROTECT) null — si sale de un turno, resta en su arqueo.
* registrado_por FK(Usuario, PROTECT). Sin campo metodo (D-06).

## Servicios
* registrar_compra(): compra + detalles + ENTRADA por producto (lock productos por id), atómico.
* pagar_proveedor(): lock compra, Σ abonos ≤ total, PAGADA al igualar.

## Pendiente
* Anular compra: estado existe, sin servicio definido.

## Plantillas
proveedor_lista, proveedor_form, compra_lista, compra_form (formset), compra_detalle.
