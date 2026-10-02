# app ventas
> Fuente: Documento 4 (BD) v1.0 + decisiones 2026-10-01. Al escribir models.py, el código pasa a ser la verdad: dejar aquí solo reglas no obvias.

## Venta — ventas (fase 7) — se crea SOLO al cobrar (D-07)
* numero_venta CharField(12) UK (V-000125) · cliente FK(Cliente, PROTECT) null (consumidor final).
* empleado FK(Empleado, PROTECT) · sesion_caja FK("caja.SesionCaja", PROTECT) · fecha DateTime índice.
* subtotal CHECK ≥0 · descuento default 0 CHECK ≤ subtotal · iva CHECK ≥0 · total CHECK ≥0 = subtotal − descuento + iva.
* estado CHECK PAGADA/ANULADA (sin PENDIENTE), índice.
* motivo_anulacion CharField(200) null · fecha_anulacion null · anulada_por FK(Usuario, PROTECT) null.
* P1 (decidido, falta campo): turno del que sale la devolución → propuesta sesion_caja_devolucion FK("caja.SesionCaja", PROTECT) null. Confirmar al modelar.

## DetalleVenta — detalles_venta
* venta FK(Venta, CASCADE) · producto FK(Producto, PROTECT) · cantidad PositiveInt CHECK >0.
* precio_unitario CHECK ≥0 y porcentaje_iva (copias, RN-09) · subtotal. UNIQUE(venta, producto).

## Factura — facturas
* venta OneToOne(Venta, PROTECT) · prefijo CharField(5) (FV) · numero PositiveInt · UNIQUE(prefijo, numero).
* fecha_emision · total · estado CHECK VIGENTE/ANULADA.

## Consecutivo — consecutivos (D-10)
* prefijo CharField(5) UK (V, FV, RC) · descripcion CharField(50) · ultimo_numero PositiveInt CHECK ≥0.
* Migración de datos: V, FV, RC en 0.

## Servicios
* siguiente_numero(prefijo): select_for_update + 1, dentro de la transacción del llamador.
* registrar_venta(): atómico. Locks: turno → productos por id → consecutivos (V, FV, RC). Crea venta, detalles, pago, factura, SALIDAs.
* anular_venta(): solo ADMIN. ADMIN elige turno ABIERTO del que sale el efectivo devuelto (P1); sin turno abierto no se anula. Locks: turno → venta → productos por id. Venta y factura ANULADA + ENTRADA/ANULACION.
* exceptions.py: StockInsuficiente, TurnoCerrado, VentaYaAnulada, EfectivoInsuficiente.

## Punto de venta (P2 decidido)
* Carrito en la sesión de Django; cada acción (agregar, quitar, corregir, cliente) = POST + recarga.
* JS mínimo (pos.js) solo para calcular el cambio. Código con foco automático (RNF-11).
* Cancelar = limpiar sesión. StockInsuficiente al cobrar → carrito intacto.

## Pendiente
* Descuento frente a IVA (¿antes del IVA y repartido por línea?) — confirmar con contador.

## Plantillas
pos, venta_lista, venta_detalle, factura (print.css carta/80 mm), mis_compras.
