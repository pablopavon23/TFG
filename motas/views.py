# To manage HttpResponses:
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.template import Context
# To manage templates:
from django.template.loader import get_template
# For security:
from django.views.decorators.csrf import csrf_exempt
from django.template.context_processors import csrf
# To authenticate users:
from django.contrib.auth import logout, authenticate, login
# Importamos los modelos:
from .models import *
# Importamos el parseador:
# from .parser_SQL import parser_function
from cgi import parse_qs
# ------------------------------------------------------------------------------

# Create your views here.
@csrf_exempt
def user_login(request):
    print(request)
    # Para imprimir la url sobre la que se hace la peticion
    print(request.path)
    # print(request.method)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        # print(user) #Si es un usuario valido me devuelve el nombre,sino da 'none'

        if user is None: #Es usuario no valido
            return redirect('/register')
        else:
            login(request,user)
            new_url = '/'+str(user)+'/index'
            return redirect(new_url)

    else:
        contexto = Context({})
        return render(request,'login.html',contexto)

# ------------------------------------------------------------------------------

def register(request):
    contexto = Context({'Registro':"Hola"})
    return render(request,'register.html',contexto)
    # return HttpResponse("Hello people")

# ------------------------------------------------------------------------------

@csrf_exempt
def index(request, peticion):
    print(request)
    print("Se realiza la peticion: "+peticion)

    if peticion == "urjc" or peticion == "ciemat":  # Tienen acceso total
        plantilla = "index_all.html"
    elif peticion == "com_mad":  # Tiene acceso solo a ClinicaFuenlabrada
        plantilla = "index_CF.html"
    else:   # Cualquiera otra sera slices, tables o maps
        plantilla = peticion+'.html'

    contexto = Context({'Indice':"Hola"})
    return render(request,plantilla,contexto)
    # return HttpResponse("Hello people")

# ------------------------------------------------------------------------------

def slices(request, peticion):
    contexto = Context({'Graficos':"Hola"})
    return render(request,'slices.html',contexto)
    # return HttpResponse("Hello people")

# ------------------------------------------------------------------------------

@csrf_exempt
def tables(request, peticion):
    contexto = Context({'TablasDatos':"Hola"})
    return render(request,'tables.html',contexto)
    # return HttpResponse("Hello people")

# ------------------------------------------------------------------------------

def leaflet(request, peticion):
    print(request)  #Esto devuelve <WSGIRequest: GET '/leaflet_ED70.html'>
    # if request == <WSGIRequest: GET '/leaflet_ED70.html'>:
    #     print("helo")
    # solicitud = request.split(" ")
    # print(solicitud[2])
    contexto = Context({'Mapas':"Hola"})
    return render(request,'leaflet_ED70.html',contexto)
    # return HttpResponse("Hello people")

# ------------------------------------------------------------------------------

def maps(request):
    contexto = Context({'Mapas2':"Hola"})
    return render(request,'maps.html',contexto)
    # return HttpResponse("Hello people")
