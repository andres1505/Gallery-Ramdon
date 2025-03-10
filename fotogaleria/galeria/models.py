from django.db import models
from django.utils import timezone#Manenja fechas y horas

# Create your models here.
class Foto(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='fotos/')
    fecha_subida = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-fecha_subida']  # Ordenar por fecha (las más recientes primero)
        verbose_name = 'Foto'
        verbose_name_plural = 'Fotos'
        
    def __str__(self):
        return self.titulo
    
    def tiempo_desde_subida(self):
        """Retorna el tiempo transcurrido desde la subida en un formato legible"""
        ahora = timezone.now()
        diferencia = ahora - self.fecha_subida
        
        if diferencia.days > 0:
            if diferencia.days == 1:
                return "1 día"
            else:
                return f"{diferencia.days} días"
        
        horas = diferencia.seconds // 3600
        if horas > 0:
            if horas == 1:
                return "1 hora"
            else:
                return f"{horas} horas"
        
        minutos = diferencia.seconds // 60
        if minutos == 1:
            return "1 min"
        else:
            return f"{minutos} mins"