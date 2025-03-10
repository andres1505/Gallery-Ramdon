from django.contrib import admin
from .models import Articulo

# Register your models here.
@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_publicacion', 'publicada')
    list_filter = ('publicada', 'fecha_publicacion')
    search_fields = ('titulo', 'resumen')