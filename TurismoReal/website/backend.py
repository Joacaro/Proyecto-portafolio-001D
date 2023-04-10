from django.contrib.auth.backends import BaseBackend
from django.conf import settings
from django.db import connections
from .models import Cliente

class MyBackend(BaseBackend):
    def authenticate(self, request, username: None, password: None):
        with connections['default'].cursor() as cursor:
            try:
                cliente = Cliente.objects.filter(email=username, clave=password).get()
                return cliente
            except Exception as ex:
                print(ex)
                return None