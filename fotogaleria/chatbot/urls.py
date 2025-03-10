from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.lista_personajes, name='lista_personajes'),
    path('personaje/<int:personaje_id>/', views.detalle_personaje, name='detalle_personaje'),
    path('personaje/<int:personaje_id>/enviar/', views.enviar_mensaje, name='enviar_mensaje'),
    path('historial/', views.historial_conversaciones, name='historial_conversaciones'),
    path('conversacion/<int:conversacion_id>/', views.ver_conversacion, name='ver_conversacion'),
]