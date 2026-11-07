from django import forms
from django.db.models import Q
from apps.core.forms import BootstrapFormMixin
from apps.productos.models import Categoria, Producto

class CategoriaForm(BootstrapFormMixin, forms.ModelForm):
    """ Formulario para crear o editar una categoria de productos. """
    # No es necesario definir campos aqui por que los heredamos del modelo 
    class Meta:
        model = Categoria
        fields = ["nombre", "descripcion"]
        widgets = {
            "nombre": forms.TextInput(attrs={"placeholder": "Nombre de la categoria"}),
            "descripcion": forms.Textarea(
                attrs={"placeholder": "Descripcion de la categoria", "rows":3}
            )
        }
        



class ProductoForm(BootstrapFormMixin, forms.ModelForm):
    """ Formulario para crear o editar un producto, """
    class Meta:
        model = Producto
        fields = [
            "codigo", "nombre", "descripcion", "categoria", "proveedor", "precio_compra",
            "porcentaje_iva", "clasificacion_iva", "precio_venta", "imagen"
        ]
        widgets = {"descripcion": forms.Textarea(attrs={"placeholder": "Descripción del producto", "rows":3})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["categoria"].queryset = Categoria.objects.filter(
            Q(activo=True) | Q(pk=self.instance.categoria_id)
        )
