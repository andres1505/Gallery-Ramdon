
from django.db import models
from django.contrib.auth.models import User

class Personaje(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='personajes/')
    personalidad = models.TextField(help_text="Descripción de la personalidad para generar respuestas")
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre

class Conversacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    personaje = models.ForeignKey(Personaje, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    titulo = models.CharField(max_length=200, default="Nueva conversación")
    
    def __str__(self):
        return f"{self.personaje.nombre} - {self.titulo}"

class Mensaje(models.Model):
    USUARIO = 'usuario'
    PERSONAJE = 'personaje'
    TIPO_CHOICES = [
        (USUARIO, 'Usuario'),
        (PERSONAJE, 'Personaje'),
    ]
    
    conversacion = models.ForeignKey(Conversacion, on_delete=models.CASCADE, related_name='mensajes')
    texto = models.TextField()
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    fecha = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['fecha']
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.texto[:50]}"