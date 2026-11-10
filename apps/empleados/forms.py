from django import forms
from apps.core.forms import BootstrapFormMixin
from apps.empleados.models import Cargo

class CargoForm(BootstrapFormMixin, forms.ModelForm):
   """ Formulario para crear o editar un cargo """
   class Meta:
       model = Cargo
       fields = ["nombre", "salario_base", "descripcion"]
       widgets ={
            "descripcion" : forms.Textarea(attrs={"placeholder": "Decripcion del cargo", "rows":3})
       }
