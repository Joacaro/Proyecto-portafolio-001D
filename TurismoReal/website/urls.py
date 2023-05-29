from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path("", views.index, name="index"),

    path("login", views.login, name="login"),
    path("crearcliente", views.crearcliente, name="crearcliente"),
    path('welcome',views.welcome , name="welcome"), 
    path('salir', views.salir, name="salir"),
]