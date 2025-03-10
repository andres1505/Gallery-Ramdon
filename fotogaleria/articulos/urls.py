from django.urls import path
from . import views

app_name = 'articulos'

urlpatterns = [
    path('', views.lista_articulos, name='lista_articulos'),
    path('<int:articulo_id>/', views.detalle_articulo, name='detalle_articulo'),
]