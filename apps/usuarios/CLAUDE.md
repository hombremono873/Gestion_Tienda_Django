# app usuarios
> Fuente: Documento 4 (BD) v1.0 + decisiones 2026-10-01. Al escribir models.py, el código pasa a ser la verdad: dejar aquí solo reglas no obvias.

## Usuario(AbstractUser) — db_table usuarios — AUTH_USER_MODEL
* email EmailField UK — USERNAME_FIELD (login por email, D-09).
* tipo_documento CharField(3) CHECK CC/CE/TI/NIT/PP · numero_documento CharField(20) solo dígitos.
* telefono CharField(20) null · rol CharField(10) CHECK ADMIN/EMPLEADO/CLIENTE.
* Heredados: password, first_name, last_name, is_active, is_staff, is_superuser, last_login, date_joined.
* Constraints: UNIQUE(email), UNIQUE(tipo_documento, numero_documento), CHECK rol.

## Reglas
* Definir ANTES del primer migrate (y sobre PostgreSQL). Decidir qué hacer con `username`.
* Manager propio por email. Superuser → rol ADMIN.
* UN solo rol por cuenta (D-09). Empleado que compra = Cliente sin cuenta (P3, opción A).
* Cuentas se desactivan (is_active=False), nunca se borran (RN-16).

## Servicios (services.py, fase 3)
* registrar_cliente(): Usuario rol CLIENTE + Cliente, atómico.
* alta_empleado(): Usuario rol EMPLEADO + Empleado, atómico.

## Plantillas
login, registro, perfil, password_reset.
