# app empleados
> Fuente: Documento 4 (BD) v1.0 + decisiones 2026-10-01. Al escribir models.py, el código pasa a ser la verdad: dejar aquí solo reglas no obvias.

## Cargo — cargos (fase 2)
* nombre CharField(80) UK · salario_base Dec(12,2) CHECK ≥0 · descripcion Text null.

## Empleado — empleados (fase 3)
* usuario OneToOne(Usuario, PROTECT) — rol EMPLEADO o ADMIN.
* cargo FK(Cargo, PROTECT) · fecha_ingreso Date · salario Dec CHECK ≥0 (puede ≠ salario_base).
* estado CHECK ACTIVO/RETIRADO.

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
