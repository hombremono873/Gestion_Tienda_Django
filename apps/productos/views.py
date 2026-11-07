from django.contrib import messages
from django.views import View
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from apps.productos.models import Categoria, Producto
from apps.core.constantes import Rol
from apps.core.mixins import RolRequeridoMixins
from django.contrib.messages.views import SuccessMessageMixin
from apps.productos.forms import CategoriaForm, ProductoForm
from django.urls import reverse_lazy
from django.shortcuts import redirect
# Create your views here.
#Nota solo lista las categorías por lo que no se conecta al formulario

# No requiere conexion con el formulario
class CategoriaView(RolRequeridoMixins, ListView):
    """ vista para listar las categorías de productos """
    model = Categoria
    template_name = "productos/categoria_list.html"
    roles_permitidos = [Rol.ADMIN]
    context_object_name = "categorias"

# Requiere conexion con el formulario
class CategoriaCreateView(RolRequeridoMixins, SuccessMessageMixin, CreateView):
    """ vista para crear un nueva categoría de productos """
    model = Categoria
    template_name = "productos/categoria_form.html"
    form_class = CategoriaForm
    roles_permitidos = [Rol.ADMIN]
    success_message = "Categoría creada correctamente"
    success_url = reverse_lazy("productos:categoria_list")

# Requiere conexion con el formulario
class CategoriaUpdateView(RolRequeridoMixins, SuccessMessageMixin, UpdateView):
    """ Vista para actualizar una categoria de productos """
    model = Categoria
    template_name = "productos/categoria_form.html"
    form_class = CategoriaForm
    roles_permitidos = [Rol.ADMIN]  
    success_message = "Categoría actualizada correctamente"
    success_url = reverse_lazy("productos:categoria_list")

class CategoriaDesactivateView(RolRequeridoMixins, SingleObjectMixin, View):
    """ Vista para activar o desactivar una categoría (borrado lógico, RN-16). Solo acepta POST """
    model = Categoria
    roles_permitidos = [Rol.ADMIN]

    def post(self, request, *args, **kwargs):
        """ Sobreescribimos el metodo post para desactivar la categoria en lugar de eliminarla """
        categoria = self.get_object()

        categoria.activo = not categoria.activo
        categoria.save(update_fields=["activo"])
        estado = "activada" if categoria.activo else "desactivada"
        messages.success(request, f"Categoría {estado} correctamente")
        return redirect("productos:categoria_list")
    
class ProductoView(RolRequeridoMixins, ListView):
    """ Vista para listar los productos """
    model = Producto
    template_name = "productos/producto_list.html"
    roles_permitidos = [Rol.ADMIN]
    context_object_name = "productos"

class ProductoCreateView(RolRequeridoMixins, SuccessMessageMixin, CreateView):
    """ Vista para crear un nuevo producto """
    model = Producto
    template_name = "productos/producto_form.html"
    form_class = ProductoForm
    roles_permitidos = [Rol.ADMIN]
    success_message = "Producto creado correctamente"
    success_url = reverse_lazy("productos:producto_list")

class ProductoUpdateView(RolRequeridoMixins, SuccessMessageMixin, UpdateView):
    """ Vista para actualizar un producto """

    model = Producto
    template_name = "productos/producto_form.html"
    form_class = ProductoForm
    roles_permitidos = [Rol.ADMIN]
    success_message = "Producto actualizado correctamente"
    success_url = reverse_lazy("productos:producto_list")

class ProductoDesactivateView(RolRequeridoMixins, SingleObjectMixin, View):
    """ Vista para activar o desactivar un producto (Borrado lógico, RN-16) """
    model = Producto
    roles_permitidos = [Rol.ADMIN]

    def post(self, request, *args, **kwargs):
        """Sobreescribimos el método post para desactivar el producto en lugar de eliminarlo """
        producto = self.get_object() #Busca en la base de datos el producto cuyo pk viene en la dirección y lo devuelve.
        producto.activo = not producto.activo
        producto.save(update_fields=["activo"])

        if producto.activo:
            messages.success(request, "Producto activado correctamente")
        else:
            messages.success(request, "Producto desactivado correctamente")
        return redirect("productos:producto_list")