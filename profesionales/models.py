from django.db import models


class Oftalmologo(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    matricula = models.CharField(max_length=20)

    class TipoMatricula(models.TextChoices):
        MP= "MP", "Matricula Provincial"
        MN= "MN", "Matricula Nacional"

    tipo_matricula= models.CharField(max_length=2, choices=TipoMatricula)
    
    class Meta:
        ordering = ["apellido", "nombre"]
        constraints = [ 
            models.UniqueConstraint(
                fields=["tipo_matricula", "matricula"],
                name="oftalmologo_matricula_unica",
            )
        ]

    def __str__(self):
        return f"{self.apellido}, {self.nombre} ({self.tipo_matricula} {self.matricula})"

    def save(self, *args, **kwargs):
        self.matricula = self.matricula.replace(".", "").replace(" ", "")
        super().save(*args, **kwargs)
