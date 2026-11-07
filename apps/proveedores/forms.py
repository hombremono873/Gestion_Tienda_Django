from django import forms
from apps.core.forms import BootstrapFormMixin
from apps.proveedores.models import Proveedor

class ProveedorForm(BootstrapFormMixin, forms.ModelForm):
    """ Formulario para crear o editar un proveedor. """

    class Meta:
        model = Proveedor
        fields = ["nit", "razon_social", "contacto", "telefono", "direccion"]
        default_widgets = {
              "nit": forms.TextInput(attrs={"placeholder": "Ej: 900123456-7"}),
        }