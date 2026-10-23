from django.urls import path

from . import views
from .views import RegistroView, IngresoView, SalirView

app_name = 'usuarios'

urlpatterns = [
    path("registro/", RegistroView.as_view(), name="registro" ),
    path("login/", IngresoView.as_view(), name="login" ),
    path("salir/", SalirView.as_view(), name="salir" )
]
