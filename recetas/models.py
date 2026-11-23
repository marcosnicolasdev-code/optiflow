from decimal import Decimal
from datetime import date

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models


class GraduacionOjo(models.Model):
    class Ojo(models.TextChoices):
        OD= "OD", "Ojo Derecho"
        OI= "OI", "Ojo Izquierdo"
    
    ojo = models.CharField(max_length=2, choices=Ojo)
    esfera = models.DecimalField(max_digits=4, decimal_places=2)
    cilindro = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    eje = models.PositiveSmallIntegerField(null=True, blank=True, validators=[MaxValueValidator(180)])
    adicion = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)

    def clean(self):
        super().clean()
        
        if self.cilindro == 0:
            self.cilindro = None

        errores = {}

        #Lo siguiente, permite que esfera, cilindro y adición vayan de 0,25 en 0,25
        paso = Decimal("0.25")
        for campo in ("esfera", "cilindro", "adicion"):
            #getattr evita codigo extenso y tener que repetir el if varias veces
            valor = getattr(self, campo)
            if valor is not None and valor % paso != 0:
                errores[campo] = "Debe ir en pasos de 0,25"

        #Si hay cilindro, el eje es obligatorio 
        if self.cilindro is not None and self.eje is None:
            errores["eje"] = "El eje es obligatorio cuando hay cilindro."

        #Si no hay cilindro el eje debe estar vacio
        if self.cilindro is None and self.eje is not None:
            errores["eje"] = "El eje debe quedar vacio si no hay cilindro."

        if errores:
            raise ValidationError(errores)
        
    class Meta:
        abstract = True

    
class Receta(models.Model):
    class Diagnostico(models.TextChoices):
        MIOPIA= "MIOPIA", "Miopía"
        HIPERMETROPIA= "HIPERMETROPIA", "Hipermetropía"
        ASTIGMATISMO= "ASTIGMATISMO", "Astigmatismo"
        PRESBICIA= "PRESBICIA", "Presbicia"
        AMETROPIA= "AMETROPIA", "Ametropia"
        ESTRABISMO= "ESTRABISMO", "Estrabismo"
        ANISOMETROPIA= "ANISOMETROPIA", "Anisometropía"

    
    cliente = models.ForeignKey("clientes.Cliente", on_delete=models.PROTECT, related_name="recetas")
    oftalmologo = models.ForeignKey("profesionales.Oftalmologo", on_delete=models.PROTECT, related_name="recetas")
    fecha_receta = models.DateField(default=date.today, null=True, blank=True)
    diagnostico = models.CharField(max_length=20, blank=True, choices=Diagnostico)
    firmada = models.BooleanField("con firma y sello", default=False)
    obra_social = models.CharField(max_length=100, blank=True)
    observaciones_receta = models.TextField(blank=True)

    class Meta:
        ordering = ["-fecha_receta", "-id"]
        
    def __str__(self):
        fecha = self.fecha_receta or "sin fecha"
        return f"Receta de {self.cliente} ({fecha})"

    #Verificador de recetas completas
    def faltantes_legales(self):
        faltan = []
        if not self.fecha_receta:
            faltan.append("fecha")
        if not self.diagnostico:
            faltan.append("diagnóstico")
        if not self.firmada:
            faltan.append("firma y sello")
        return faltan
    
class RecetaOjo(GraduacionOjo):
    class Distancia(models.TextChoices):
        LEJOS = "LEJOS", "Lejos"
        CERCA = "CERCA", "Cerca"

    receta = models.ForeignKey("recetas.Receta", on_delete=models.CASCADE, related_name="ojos")
    distancia = models.CharField(max_length=5, choices=Distancia, default=Distancia.LEJOS)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["receta", "ojo", "distancia"],
                name="receta_ojo_distancia_unica",
            )
        ] 

    def __str__(self):
        return f"{self.ojo} {self.get_distancia_display()} - {self.receta})"


