from email.policy import default
from pyexpat import model
from unittest.util import _MAX_LENGTH
from django.db import models
from datetime import datetime  
# Create your models here.

class Cliente(models.Model):
    id_cli = models.IntegerField(primary_key=True, db_column="id_cli")
    tipo_vat = models.IntegerField(db_column="tipo_vat")
    vat = models.CharField(max_length=10, db_column="vat")
    nombre_cli = models.CharField(max_length=50)
    apaterno_cli = models.CharField(max_length=50)
    amaterno_cli = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    telefono = models.CharField(max_length=10)
    edad_cli = models.IntegerField
    sexo_cli = models.CharField(max_length=10)
    direccion_cli = models.CharField(max_length=100)
    estadocivil_cli = models.CharField(max_length=50)
    clave=models.CharField(max_length=64, db_column="clave")
    last_login = models.DateTimeField(default=datetime.now, blank=True)
    _is_active = models.BooleanField(default = False,db_column="is_active")
    is_authenticated = models.BooleanField(default = False,db_column="is_authenticated")

    class Meta:
        managed=False
        db_table = 'Cliente'