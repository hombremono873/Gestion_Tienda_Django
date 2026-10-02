# Gestiontienda

Sistema de gestión de tienda (ventas, inventario, caja, proveedores, empleados) con Django y Foundation.

## Puesta en marcha

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
# crear .env con SECRET_KEY, DEBUG y ALLOWED_HOSTS
python manage.py migrate
python manage.py runserver
```

## Estructura

- `config/` — configuración del proyecto (settings, urls, wsgi, asgi)
- `apps/` — una app por dominio: core, usuarios, clientes, empleados, productos, inventario, proveedores, ventas, caja, reportes
- `templates/` — `base.html`, parciales y una carpeta por app
- `static/` — Foundation, jQuery, estilos y JS propios
- `media/` — archivos subidos (imágenes de productos)
