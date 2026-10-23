from django.shortcuts import render
from .forms import RegistroForm, LoginForm
from .services import registrarse, VinculoError
from django.views.generic import FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.contrib.auth import login
from django.urls import reverse_lazy
# Create your views here.

class RegistroView(FormView):
    template_name = "usuarios/registro.html"
    form_class = RegistroForm
    success_url = reverse_lazy("core:inicio")

    def form_valid(self, form):
        try:
            usuario = registrarse(form.cleaned_data)
        except VinculoError as e:
            form.add_error(None, str(e))
            return self.form_invalid(form)
        login(self.request, usuario)
        messages.success(self.request, "Cuenta creada. ¡Bienvenido a TiendaGest!")
        return super().form_valid(form)   

class IngresoView(LoginView):
    template_name = "usuarios/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True
    next_page = "core:inicio"

class SalirView(LogoutView):
    next_page=reverse_lazy("core:inicio")  #Pendiente defirnir la salida


      