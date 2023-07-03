from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import loginform
from django.db import connections
import cx_Oracle as oracledb
import hashlib
from .backend import MyBackend
from django.contrib.auth import login as auth_login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from math import ceil
from .models import Departamento
mybackend = MyBackend()
# Create your views here.
def error_404(request, exception):
    return render(request, 'turismoreal/404.html')
def index(request):
    return render(request, 'turismoreal/index.html')
def cartas(request):
    event_list = Departamento.objects.all()
    return render(request, 'turismoreal/carta.html', {'event_list': event_list})
def salir(request):
    logout(request)
    return redirect("login")
def correoreserva(usuario,depto,correopersona):
    send_mail(
        'Confirmacion de reserva',
        'Señor/a '+ usuario+ ' su reserva fue confirmada, en el departamento '+depto,
        settings.EMAIL_HOST_USER,
        [correopersona],
        fail_silently=False
    )
    return correoreserva
def correocancelacion(usuario,correopersona):
    send_mail(
        'Se ha cancelado la reserva',
        'Señor/a '+ usuario+ ' su reserva fue cancelada, para hacer una nueva reserva visitenos en www.turismoreal.cl',
        settings.EMAIL_HOST_USER,
        [correopersona],
        fail_silently=False
    )
    return correocancelacion    

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
        ref_cursor = connection.cursor()
        cursor.callproc("SP_Cliente_VAL", [ref_cursor,prut,pemail])
        resultado = []
        for row in ref_cursor:
            resultado.append(row)
            if resultado[0][0]==prut: 
                validar=True
                break
            elif resultado[0][1]==pemail:
                validar=True
                break
        if validar==None:
            registro=True   
            cursor.callproc('SP_Clientes_Mant', [prut, pnombre, papellidop, papellidom, pedad, psexo, pdireccion, pestadocivil, ptelefono, pemail, hash])
        connection.commit()  
        cursor.close()
        connection.close()
    return render(request, 'turismoreal/crearcliente.html',{"validar":validar,"registro":registro})

def editarcliente(request):
    registro=None
    validar=None
    if request.method == "POST":
        datos=request.POST
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
        ref_cursor = connection.cursor()
        cursor.callproc("SP_Cliente_Val", [ref_cursor,None,pemail])
       
        resultado = []
        
        for row in ref_cursor:
            
            resultado.append(row)
            
            if resultado[0][1]==pemail:
                validar=True
                break

        if validar==None:
            registro=True 
            cursor.callproc('SP_Clientes_Update', [pnombre, papellidop, papellidom, pedad, psexo, pdireccion, pestadocivil, ptelefono, pemail, hash])
        connection.commit()  
        cursor.close()
        connection.close()
    return render(request, 'turismoreal/crearcliente.html',{"validar":validar,"registro":registro})

def login(request):
    mensaje=None
    form = loginform(data=request.POST)
    if request.method == "POST":
        if form.is_valid():
            usuario = form.cleaned_data["email"]
            clave = form.cleaned_data["clave"]
            hash = hashlib.sha256(clave.encode('utf-8')).hexdigest()
            user = mybackend.authenticate(
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

def listarcartas(request):
    connection = oracledb.connect(user="c##deptos", password="dbadmin23", encoding="UTF-8")
    pagina=1
    try:
        pagina=int(request.GET["pagina"])
    except:
        pagina=1
    cursor = connection.cursor()
    salto=(pagina-1)*8
    tomar=salto+8
    ref_cursor = connection.cursor()
    cursor.callproc("SP_Dept_List", [ref_cursor])
    resultado = {"cartas": []}
    for row in ref_cursor:
        resultado["cartas"].append(row)
    total=len(resultado["cartas"])
    total=ceil(total/8)

    resultado1 = {"cartas": []}
    resultado1["cartas"]=resultado["cartas"][salto:tomar]
    resultado1["total"]=total
    return JsonResponse(resultado1, safe=False)

@login_required(login_url="login")
def welcome(request):
    return render(request, 'turismoreal/welcome.html')

@login_required(login_url="login")
def reserva(request):
    if request.method == "POST":
        connection = oracledb.connect(user="C##deptos", password="dbadmin23",
                                  encoding="UTF-8")
        
        
def eliminar_reserva(request):
    if request.method == "POST":
        connection = oracledb.connect(user="C##deptos", password="dbadmin23",
                                  encoding="UTF-8")
        cursor = connection.cursor()
        ref_cursor = connection.cursor()
        cursor.callproc("SP_Arriendos_Eliminar", [ref_cursor,request.user.id])
    
        resultado=[]                  
        for row in ref_cursor:
            print(row)
            resultado.append(row[1])
        dat1=row[0]
        correocancelacion(request.user.nombre,request.user.email)
        cursor.callproc("SP_registros_mesas_d", dat1)
        return redirect("clientes/welcome")