from django.db import models
from datetime import date


class Cliente(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    dni = models.CharField(max_length=20, unique=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    fecha_alta = models.DateField(default=date.today)
    telefono = models.CharField(max_length=20)
    usuario_lentes = models.BooleanField(default=False)
    marca_previa = models.CharField(max_length=50, blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["apellido", "nombre"]

    def __str__(self):
        return f"{self.apellido}, {self.nombre} ({self.dni})"

    def save(self, *args, **kwargs):
        self.dni = self.dni.replace(".", "").replace(" ", "")
        super().save(*args, **kwargs)