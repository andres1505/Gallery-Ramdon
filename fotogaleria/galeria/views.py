from django.shortcuts import render
from .models import Foto

# Create your views here.
#aca se define la vista principal
def inicio(request):
    fotos = Foto.objects.all()
    return render(request, 'layouts/inicio.html', {'fotos': fotos})

# 