from django import template
from django.template.defaultfilters import floatformat

register = template.Library()


@register.filter
def cop(valor):
    """Muestra un valor en pesos colombianos, por ejemplo $ 12.500. Solo cambia cómo se ve."""
    if valor in (None, ""):
        return ""
    return f"$ {floatformat(valor, '-2g')}"
