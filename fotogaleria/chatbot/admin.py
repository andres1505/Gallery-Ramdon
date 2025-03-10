from django.contrib import admin
from .models import Personaje, Conversacion, Mensaje
# Register your models here.

@admin.register(Personaje)
class PersonajeAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo')
    search_fields = ('nombre', 'descripcion')

@admin.register(Conversacion)
class ConversacionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'personaje', 'usuario', 'fecha_creacion')
    list_filter = ('personaje', 'fecha_creacion')

@admin.register(Mensaje)
class MensajeAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'texto_truncado', 'conversacion', 'fecha')
    list_filter = ('tipo', 'fecha')
    
    def texto_truncado(self, obj):
        return obj.texto[:50] + '...' if len(obj.texto) > 50 else obj.texto
    texto_truncado.short_description = 'Texto'