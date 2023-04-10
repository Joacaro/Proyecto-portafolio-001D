from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import loginform
import hashlib
from .backend import MyBackend
from django.contrib.auth import login as auth_login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
def error_404(request, exception):
    return render(request, 'turismoreal/404.html')
def index(request):
    return render(request, 'turismoreal/index.html')

def welcome(request):
    return render(request, "turismoreal/welcome.html")

def crearcliente(request):
    if request.method == "POST":
        registro = UserCreationForm(request.POST)
        if registro.is_valid():
            registro.save()
            usuario=registro.cleaned_data["email"]
            clave=registro.cleaned_data["clave"]
            user = authenticate(username=usuario, password=clave)
            try:
                login(request, user)
                return redirect("cliente/login")
            except Exception as ex:
                print(ex)
        else:
            registro = UserCreationForm()
    return render(request, 'crearcliente.html', {'registro':registro})

def login(request):
    mensaje=None
    form = loginform(data=request.POST)
    if request.method == "POST":
        if form.is_valid():
            usuario = form.cleaned_data["email"]
            clave = form.cleaned_data["clave"]
            hash = hashlib.sha256(clave.encode('utf-8').hexdigest())
            user = MyBackend.authenticate(
                request, username=usuario, password=hash
            )
            if user is not None:
                try:
                    auth_login(request, user, backend='website.backend.MyBackend')
                    return redirect("cliente/welcome")
                except Exception as ex:
                    print(ex)
            else:
                mensaje=True
            print(mensaje)
    return render(request, 'turismoreal/login.html', {"form": form, "mensaje":mensaje})