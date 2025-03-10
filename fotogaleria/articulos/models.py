from django.db import models

# Create your models here.
class Articulo(models.Model):
    titulo = models.CharField(max_length=200)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    resumen = models.TextField()
    detalle = models.TextField()
    foto = models.ImageField(upload_to='noticias/')
    publicada = models.BooleanField(default=True)

    
    class Meta:
        ordering = ['-fecha_publicacion']
        
    def __str__(self):
        return self.titulo