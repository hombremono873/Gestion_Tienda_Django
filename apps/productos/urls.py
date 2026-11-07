from django.urls import path

from . import views

app_name = 'productos'

urlpatterns = [
    path('categorias/', views.CategoriaView.as_view(), name='categoria_list'),
    path('categorias/nueva/', views.CategoriaCreateView.as_view(), name='categoria_crear'),
    path('categorias/<int:pk>/editar/', views.CategoriaUpdateView.as_view(), name="categoria_editar"),
    path('categorias/<int:pk>/desactivar/', views.CategoriaDesactivateView.as_view(), name = "categoria_desactivar"),
    path('', views.ProductoView.as_view(), name="producto_list"),
    path('nuevo_producto/', views.ProductoCreateView.as_view(), name="producto_crear"),
    path('actualizar_producto/<int:pk>/', views.ProductoUpdateView.as_view(), name="producto_actualizar"),
    path('productos/<int:pk>/desactivar/', views.ProductoDesactivateView.as_view(), name="producto_desactivar"),
]
