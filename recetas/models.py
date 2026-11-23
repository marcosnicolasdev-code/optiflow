from decimal import Decimal

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

