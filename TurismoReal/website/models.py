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

class Departamento(models.Model):
    id_depto = models.IntegerField(primary_key=True, db_column="id_depto")
    n_depto = models.IntegerField(db_column="n_depto")
    cant_hab = models.IntegerField(db_column="cant_hab")
    cant_ban = models.IntegerField(db_column="cant_ban")
    disponibilidad = models.CharField(max_length=1, db_column="disponibilidad")
    mantenimiento = models.CharField(max_length=1, db_column="mantenimiento")
    valor = models.IntegerField(db_column="valor")
    direccion_ed_depto = models.CharField(max_length=50, db_column="direccion_ed_depto")
    id_tipo_comp = models.IntegerField(db_column="id_tipo_comp")
    id_inv = models.IntegerField(db_column="id_inv")
    class Meta:
        managed=False
        db_table = 'Departamento'

class Arriendo(models.Model):
    id_arriendo = models.IntegerField(primary_key=True, db_column="id_arriendo")
    fecha_inicio = models.DateField(db_column="fecha_inicio")
    fecha_fin = models.DateField(db_column="fecha_fin")
    ed_direccion_ed = models.CharField(max_length=50,db_column="ed_direccion_ed")
    cliente_id_cli = models.ForeignKey(Cliente, db_column="Cliente_id_cli",on_delete=models.CASCADE)
    class Meta:
        managed=False
        db_table = "Arriendos"