from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib import messages
from apps.core.mixins import RolRequeridoMixins
from .models import Proveedor
from apps.core.constantes import Rol
from django.urls import reverse_lazy
from django.shortcuts import redirect
from apps.proveedores.forms import ProveedorForm
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.detail import SingleObjectMixin
from django.views import View
# Create your views here.
class ProveedorView(RolRequeridoMixins, ListView):
    """ Vista para proveedores """
    template_name = "proveedores/proveedor_list.html"
    model = Proveedor
    roles_permitidos = [Rol.ADMIN]
    context_object_name = "proveedores"

class ProveedorCreateView(RolRequeridoMixins, SuccessMessageMixin, CreateView):
    """ Vista para crear un proveedor """
    template_name = "proveedores/proveedor_form.html"
    model = Proveedor
    form_class = ProveedorForm
    roles_permitidos = [Rol.ADMIN]
    success_message = "Se ha creado el proveedor correctamente"
    success_url = reverse_lazy("proveedores:proveedor_list")

class ProveedorUpdateView(RolRequeridoMixins, SuccessMessageMixin, UpdateView):
    """ Vista para actualizar un proveedor """
    template_name = "proveedores/proveedor_form.html"
    model = Proveedor
    form_class = ProveedorForm
    roles_permitidos = [Rol.ADMIN]
    success_message = "Se ha actualizado el proveedor correctamente"
    success_url = reverse_lazy("proveedores:proveedor_list")

# Cómo funciona ProveedorDeactivateView.post():
# 1. Se ejecuta cuando el botón Activar/Desactivar envía un POST a /proveedores/desactivar/<pk>/.
# 2. self.get_object() (de SingleObjectMixin) toma el pk de la URL y busca el proveedor en la
#    tabla indicada por model. Si no existe, responde 404 y el método no continúa.
# 3. "not proveedor.activo" invierte el estado: True pasa a False y False pasa a True.
# 4. save(update_fields=["activo"]) actualiza solo esa columna. El registro no se borra (RN-16).
# 5. messages.success() guarda el mensaje que se mostrará en la siguiente página.
# 6. redirect() vuelve a la lista de proveedores, donde aparece el mensaje.

class ProveedorDeactivateView(RolRequeridoMixins, SuccessMessageMixin, SingleObjectMixin, View):
    """ Vista para activar o desactivar un proveedor (borrado lógico RN-16). Solo acepta  POST"""  
    model = Proveedor
    roles_permitidos = [Rol.ADMIN]

    def post(self, request, *args, **kwargs):
        """Sobre escribimos el registro para hacer un borrado lógico """ 
        proveedor = self.get_object()  #Al activarse botton en BDD se lanza Post, se consulta BDD y retorna registro
        proveedor.activo = not proveedor.activo  # Se cambia el estado del proveedor
        proveedor.save(update_fields=["activo"])  #Se salva el estado en la BDD
        if proveedor.activo:
             messages.success(request, "Se ha activado el proveedor correctamente")
        else:
            messages.success(request, "Se ha desactivado el proveedor correctamente")      
        return redirect("proveedores:proveedor_list")    
