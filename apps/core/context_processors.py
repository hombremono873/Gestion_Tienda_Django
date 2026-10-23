"""Variables disponibles en todas las plantillas."""
from django.conf import settings


def version_estaticos(request):
    """Versión de app.css (fecha de modificación) para que el navegador no use una copia vieja."""
    ruta = settings.BASE_DIR / "static" / "css" / "app.css"
    try:
        version = int(ruta.stat().st_mtime)
    except OSError:
        version = 0
    return {"version_css": version}
