from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Foto

@admin.register(Foto)
class FotoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_subida')
    search_fields = ('titulo', 'descripcion')
    readonly_fields = ('fecha_subida',)