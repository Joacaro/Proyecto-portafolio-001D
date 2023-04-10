from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),

    path("cliente/login", views.login, name="login"),
    path("cliente/crearcliente", views.crearcliente, name="crearcliente"),
    path("cliente/welcome", views.welcome, name="welcome")

]