from django.db import models

# Create your models here.

class Cliente(models.Model):
    rut_cli = models.CharField(max_length=10, primary_key=True)
    nombre_cli = models.CharField(max_length=50)
    apellidop_cli = models.CharField(max_length=50)
    apellidom_cli = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    telefono_cli = models.CharField(max_length=10)
    edad_cli = models.IntegerField
    sexo_cli = models.CharField(max_length=10)
    direccion_cli = models.CharField(max_length=100)
    estadocivil_cli = models.CharField(max_length=50)
    clave=models.CharField(max_length=64)
