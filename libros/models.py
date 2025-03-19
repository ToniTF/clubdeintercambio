from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    dni = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return self.username

class Estado(models.Model):
    descripcion = models.CharField(max_length=100)
    
    def __str__(self):
        return self.descripcion

class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    imagen = models.ImageField(upload_to='libros/', null=True, blank=True)
    descripcion = models.TextField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='libros')
    
    def __str__(self):
        return self.titulo

class Prestamo(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='prestamos')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='prestamos')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_devolucion = models.DateTimeField(null=True, blank=True)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.libro.titulo} - {self.usuario.username}"
