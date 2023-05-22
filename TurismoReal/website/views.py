from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import loginform
from django.db import connections
import cx_Oracle as oracledb
import hashlib
from .backend import MyBackend
from django.contrib.auth import login as auth_login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.
def error_404(request, exception):
    return render(request, 'turismoreal/404.html')
def index(request):
    return render(request, 'turismoreal/index.html')
def welcome(request):
    return render(request, "turismoreal/welcome.html")
def salir(request):
    logout(request)
    return redirect("login")
def correoreserva(usuario,mesa,personas,ini,fin,correopersona):
    send_mail(
        'confirmacion de reserva',
        'señor/a '+ usuario+ ' su reserva fue confirmada, su mesa es n°'+mesa+' para '+personas+ ' personas durante '+ini +' a '+fin,
        settings.EMAIL_HOST_USER,
        [correopersona],
        fail_silently=False
    )
    return correoreserva
def correocancelacion(usuario,correopersona):
    send_mail(
        'se ha cancelado la reserva',
        'señor/a '+ usuario+ ' su reserva fue cancelada, para hacer una nueva reserva visitenos en www.restaurantsigloxxi/restaurant/home/index',
        settings.EMAIL_HOST_USER,
        [correopersona],
        fail_silently=False
    )
    return correocancelacion    

def procedimientocrearcliente(id, rut, nombre, apellido, telefono, email, clave):
    with connections['default'].cursor() as cursor:
        # parametros a enviar Sirve para CUD
        cursor.callproc("SP_clientes_c", [
                        id, rut, nombre, apellido, telefono, email, clave])
        return procedimientocrearcliente

def crearcliente(request):
    registro=None
    validar=None
    if request.method == "POST":
        datos=request.POST
        prut = datos["rut"]
        pnombre = datos["nombre"]
        papellidop = datos["apellidoP"]
        papellidom = datos["apellidoM"]
        pedad = datos["edad"]
        psexo = datos["sexo"]
        pdireccion = datos["direccion"]
        pestadocivil = datos["estado_civil"]
        ptelefono = datos["telefono"]
        pemail = datos["email"]
        pclave = datos["clave"]
        hash = hashlib.sha256(str(pclave).encode('utf-8')).hexdigest()
        connection = oracledb.connect(user="c##deptos", password="dbadmin23",
                                  encoding="UTF-8")
        cursor = connection.cursor()
        cursor.callproc('SP_Clientes', [prut, pnombre, papellidop, papellidom, pedad, psexo, pdireccion, pestadocivil, ptelefono, pemail, hash])
        connection.commit()  
        cursor.close()
        connection.close()
        return HttpResponse("Client created successfully.")
    return render(request, 'turismoreal/crearcliente.html',{"validar":validar,"registro":registro})

def login(request):
    mensaje=None
    form = loginform(data=request.POST)
    if request.method == "POST":
        if form.is_valid():
            usuario = form.cleaned_data["email"]
            clave = form.cleaned_data["clave"]
            hash = hashlib.sha256(str(clave).encode('utf-8')).hexdigest()
            user = MyBackend.authenticate(
                request, username=usuario, password=hash)
            if user is not None:
                try:
                    auth_login(request, user, backend='website.backend.MyBackend')
                    return redirect("welcome")
                except Exception as ex:
                    print(ex)
            else:
                mensaje=True
            print(mensaje)
    return render(request, 'turismoreal/login.html', {"form": form, "mensaje":mensaje})