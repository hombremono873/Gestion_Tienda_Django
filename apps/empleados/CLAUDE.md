# app empleados
> Fuente: Documento 4 (BD) v1.0 + decisiones 2026-10-01. Al escribir models.py, el código pasa a ser la verdad: dejar aquí solo reglas no obvias.

## Cargo — cargos — IMPLEMENTADO en models.py (2026-10-05)
## Empleado — empleados — IMPLEMENTADO en models.py (2026-10-05)
* Decisión propia (Doc 4 v1.1): 7 estados ACTIVO, INACTIVO, VACACIONES, LICENCIA, PERMISO, RETIRADO, SUSPENDIDO; max_length 15.
* fecha_ingreso: default=timezone.localdate (editable). NUNCA auto_now_add: es dato del negocio.
* salario puede ≠ Cargo.salario_base.
* Pendiente definir: qué estados permiten trabajar (¿abrir turno solo ACTIVO?) y relación RETIRADO ↔ Usuario.is_active.

## PagoSalario — pagos_salario (fase 9)
* empleado FK(Empleado, PROTECT) · periodo_inicio, periodo_fin Date CHECK fin ≥ inicio.
* salario_base Dec (copia) · bonificaciones Dec CHECK ≥0 default 0 · deducciones Dec CHECK ≥0.
* total_pagado CHECK ≥0 = base + bonificaciones − deducciones.
* fecha_pago Date · registrado_por FK(Usuario, PROTECT). Sin campo metodo (D-06).

## Servicios
* pagar_nomina().

## Pendiente
* ¿Nómina sale de caja? Hoy sin sesion_caja → no afecta arqueo.

## Plantillas
empleado_lista, empleado_form, nomina_lista, nomina_form, mis_pagos. Cargos: admin de Django hasta Doc 5.
