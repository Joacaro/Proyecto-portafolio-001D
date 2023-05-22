from django.contrib.auth.backends import BaseBackend
from django.conf import settings
from django.db import connections
from .models import Cliente

import cx_Oracle as oracledb
connection = oracledb.connect(user="admin_tr", password="dbadmin23", encoding="UTF-8")

class MyBackend(BaseBackend):
    def authenticate(self,username=None, password=None):
        with connections['default'].cursor() as cursor:
            try:
                cliente = Cliente.objects.filter(email=username, clave=password).get()
                return cliente
            except Exception as ex:
                print(ex)
                return None
            
    def get_user(self, id_cli):
        with connections['default'].cursor() as cursor:
            try:
                cliente =Cliente.objects.get(pk= id_cli )
                return cliente
            except :
                return None