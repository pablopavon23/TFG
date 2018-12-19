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
# Importamos el lector de la SQL:
# from .parser_SQL import executeScriptsFromFile

# Create your views here.

# ------------------------------------------------------------------------------
# Introduzco en un diccionario la lista de sitios a los que tiene acceso el usuario
def users_pages(user):
    if user == 'urjc' or user == 'ciemat':
        pages = ['ED_70','Clinica_Fuenlabrada','Lece']
    elif user == 'com_mad':
        pages = ['Clinica_Fuenlabrada']

    return pages

# ------------------------------------------------------------------------------
# Hacemos el login mostrando la pagina principal si es GET y enviando informacion
# y redirigiendo si es un POST
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
        #Si es un usuario valido me devuelve el nombre,sino da 'none'

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
# Hacemos logout y se nos redirige a la pagina principal -> login
def user_logout(request,peticion):
    # print(request)  # <WSGIRequest: GET '/urjc/logout'>
    # print(peticion) # urjc
    logout(request)
    return redirect('/')

# ------------------------------------------------------------------------------

def register(request):
    contexto = Context({'Registro':"Hola"})
    return render(request,'register.html',contexto)
    # return HttpResponse("Hello people")

# ------------------------------------------------------------------------------

@csrf_exempt
def index(request, peticion):
    # Consigo el usuario que ha accedido al portal
    user = request.user
    print("User is: "+str(user))

    # Llamo a la función que me dirá a que edificios tiene acceso ese usuario
    pages_info_user = users_pages(str(user))

    # Lo inroduzco como contexto para representarlo despues
    contexto = Context({'Builds':pages_info_user})

    return render(request,'index.html',contexto)

# ------------------------------------------------------------------------------

def slices(request, peticion):
    # Consigo el usuario que ha accedido al portal
    user = request.user
    print("User is: "+str(user))

    # Llamo a la función que me dirá a que edificios tiene acceso ese usuario
    pages_info_user = users_pages(str(user))

    # Lo inroduzco como contexto para representarlo despues
    contexto = Context({'Builds':pages_info_user})

    return render(request,'slices.html',contexto)

# ------------------------------------------------------------------------------

@csrf_exempt
def tables(request, peticion):
    # Consigo el usuario que ha accedido al portal
    user = request.user
    print("User is: "+str(user))

    # Llamo a la función que me dirá a que edificios tiene acceso ese usuario
    pages_info_user = users_pages(str(user))

    # Lo inroduzco como contexto para representarlo despues
    contexto = Context({'Builds':pages_info_user})

    return render(request,'tables.html',contexto)

# ------------------------------------------------------------------------------

def leaflet(request, peticion):
    # print(request)  # Esto devuelve <WSGIRequest: GET '/leaflet_ED70.html'>
    # print(request.path) # Esto devuelve /urjc/leaflet_ED70.html

    # -------- Esto es para conseguir saber que leaflet me estan pidiendo ----
    url = request.path
    url_leaflet = url.split('/')[2] # Obtengo leaflet_ED70, leaflet_CF o leaflet_Alm
    print(url_leaflet)

    contexto = Context({'URL':url_leaflet})
    leaf_plantilla = url_leaflet+'.html'
    # ---------------------------------------------------------------------------------------

    # Consigo el usuario que ha accedido al portal
    user = request.user
    print("User is: "+str(user))

    # Llamo a la función que me dirá a que edificios tiene acceso ese usuario
    pages_info_user = users_pages(str(user))

    # Lo inroduzco como contexto para representarlo despues
    contexto = Context({'Builds':pages_info_user})

    return render(request,leaf_plantilla,contexto)

# ------------------------------------------------------------------------------

def maps(request):
    # Consigo el usuario que ha accedido al portal
    user = request.user
    print("User is: "+str(user))

    # Llamo a la función que me dirá a que edificios tiene acceso ese usuario
    pages_info_user = users_pages(str(user))

    # Lo inroduzco como contexto para representarlo despues
    contexto = Context({'Builds':pages_info_user})

    return render(request,'maps.html',contexto)
