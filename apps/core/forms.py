from django import forms


class BootstrapFormMixin:
    """Agrega clases de Bootstrap a los campos y marca en rojo los que tienen errores."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            es_lista = isinstance(campo.widget, forms.Select)
            campo.widget.attrs["class"] = "form-select" if es_lista else "form-control"

    def full_clean(self):
        super().full_clean()
        for nombre in self.errors:
            if nombre in self.fields:
                self.fields[nombre].widget.attrs["class"] += " is-invalid"