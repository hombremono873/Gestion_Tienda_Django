# app productos
> Fuente: Documento 4 (BD) v1.0 + decisiones 2026-10-01. Al escribir models.py, el código pasa a ser la verdad: dejar aquí solo reglas no obvias.

## Categoria — categorias (fase 2)
* nombre CharField(80) UK · descripcion Text null.

## Producto — productos (fase 4)
* codigo CharField(30) UK (interno o barras) · nombre CharField(150) índice · descripcion Text null.
* categoria FK(Categoria, PROTECT) · proveedor FK("proveedores.Proveedor", SET_NULL) null.
* precio_compra, precio_venta Dec(12,2) CHECK ≥0 · porcentaje_iva Dec(5,2) CHECK ∈ {0,5,19}.
* stock PositiveInt CHECK ≥0 · stock_minimo PositiveInt CHECK ≥0 · imagen ImageField null (requiere Pillow) · activo Bool.

## Reglas
* stock NO va en formularios: solo cambia vía inventario.registrar_movimiento().
* EMPLEADO no ve precio_compra ni márgenes (RNF-10). Catálogo cliente: solo activos, sin costos (RF-08).
* Se desactiva, no se borra.

## Pendiente
* ¿Registrar compra actualiza precio_compra?

## Plantillas
producto_lista, producto_form, producto_detalle, categoria_lista, catalogo.
