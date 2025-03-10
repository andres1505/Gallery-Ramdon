from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Articulo

def lista_articulos(request):
    articulos = Articulo.objects.filter(publicada=True)
    #Vista de articulos
    return render(request, 'articulos/lista_articulos.html', {
        'articulos': articulos,
    })

def detalle_articulo(request, articulo_id):
    articulo = get_object_or_404(Articulo, id=articulo_id, publicada=True)
    return render(request, 'articulos/detalle_articulo.html', {
        'articulo': articulo,
    })