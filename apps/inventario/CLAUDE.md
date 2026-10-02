# app inventario
> Fuente: Documento 4 (BD) v1.0 + decisiones 2026-10-01. Al escribir models.py, el código pasa a ser la verdad: dejar aquí solo reglas no obvias.

## MovimientoInventario — movimientos_inventario (fase 8, tablas en bloque 6–8)
* producto FK(Producto, PROTECT) · tipo CHECK ENTRADA/SALIDA · cantidad PositiveInt CHECK >0.
* motivo CharField(20) CHECK VENTA/COMPRA/AJUSTE/ANULACION · observacion CharField(200) null.
* venta FK("ventas.Venta", PROTECT) null · compra FK("proveedores.Compra", PROTECT) null.
* usuario FK(Usuario, PROTECT) · fecha DateTime auto_now_add índice.
* Índice (producto, fecha).

## Servicios
* registrar_movimiento(): interno, SIEMPRE dentro de la transacción de quien llama; actualiza Producto.stock con F().
* ajustar_stock(): transacción propia, select_for_update del producto, motivo AJUSTE. Solo ADMIN.

## Reglas
* Stock y movimiento cambian siempre juntos.
* Venta → SALIDA/VENTA. Compra → ENTRADA/COMPRA. Anulación → ENTRADA/ANULACION.
* Dependencia circular: FK hacia ventas y compras, y esos servicios escriben aquí → FKs con texto.

## Plantillas
movimientos_lista, ajuste_form, stock_bajo.
