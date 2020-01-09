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
# Importamos el archivo y función que reside en el mismo para cargar medidas:
# from .load_medidas import get_medidas;
from .genera_medidas import get_CF_info, get_medidas_true;
# Para trabajar con JSON:
import json
import os

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

    # Proceso la solicitud
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is None: # Es usuario no válido
            return redirect('/register')
        else: # Es usuario válido
            login(request,user)
            new_url = '/'+str(user)+'/index'
            return redirect(new_url)
    else:
        contexto = {'Login':"Hola"}
        return render(request,'login.html',contexto)

# ------------------------------------------------------------------------------
# Hacemos logout y se nos redirige a la pagina principal -> login
def user_logout(request,peticion):
    logout(request)
    return redirect('/')

# ------------------------------------------------------------------------------

def register(request):
    contexto = {'Registro':"Hola"}
    return render(request,'register.html',contexto)
    # return HttpResponse("Hello people")

# ------------------------------------------------------------------------------

@csrf_exempt
def index(request, peticion):
    # Consigo el usuario que ha accedido al portal
    user = request.user

    # Llamo a la función que me dirá a que edificios tiene acceso ese usuario
    pages_info_user = users_pages(str(user))

    # Esto genera los JSON
    get_medidas_true()

    # Lo inroduzco como contexto para representarlo despues
    contexto = {'Builds':pages_info_user, 'User': user}
    return render(request,'index.html',contexto)

# ------------------------------------------------------------------------------
# Funcion que recibe como argumento el tipo de medida y los datos y devuelve un boolean indicando si
# hay valores anómalos o no.
def check_medida(tipo,medidas_test):

    if tipo == 'temperatura':
        check_tipo = "TMPaire"
    elif tipo == 'dioxido':
        check_tipo = "CO2"
    elif tipo == 'humedad':
        check_tipo = "HUMEDAD"

    # Comprobamos cada medida:
    muestras = []
    current = []
    for medidas in medidas_test:    # medidas es cada uno de los diccionarios
        current = medidas.get(check_tipo)
        if (current != None):   # Si no tenemos medida no se añade
            muestras.append(medida)

    # Ordeno las muestras para que queden de min. valor a max. valor
    muestras = sorted(muestras)
    # Compruebo si hay (o no) alerta
    if (muestras[0] < 0.0) or (muestras[len(muestras)-1] > 50.0):
        alertar = True
    else:
        alertar = False

    return alertar

# ------------------------------------------------------------------------------
#     """ La función aqui es devolver si hay que alertar o no"""
def check_values(medidas_test):
    # Invoco a la funcion que me indica si una medida cualquiera contiene valor anomalo o no
    alertar_TMP = check_medida('temperatura',medidas_test)
    alertar_CO = check_medida('dioxido',medidas_test)
    alertar_HU = check_medida('humedad',medidas_test)

    if (not alertar_TMP) and (not alertar_CO) and (not alertar_HU):
        alertar = False
    else:
        alertar = True

    return alertar

# ------------------------------------------------------------------------------

def insert_idMota(medidas_test):
    cant_motas = []   # Inicializo la lista donde guardare mota1, mota2...
    for medidas in medidas_test:    # medidas es cada uno de los diccionarios
        id_mota = medidas.get("id_mota")  # esto me permite saber que id de mota tengo
        if not str(id_mota) in cant_motas:  # asi me aseguro no guardar dos veces la misma mota.
            cant_motas.append(str(id_mota))

    # Ordeno las motas para que se muestren en orden
    cant_motas = sorted(cant_motas,key=int)

    return cant_motas

# ------------------------------------------------------------------------------
# Aquí cargo la información del JSON
def get_data():
    dir = '/home/ppp23/Escritorio/TFG/data'
    with open(os.path.join(dir, 'medidas.json')) as file: #-- Esto por si quiero meterlo en un directorio distinto al que me encuentro
        data = json.load(file)

    return data

# ------------------------------------------------------------------------------
# Proceso solicitud del POST recibido de slices pidiendo mota y medidas concretas
def procesolicitud(mota,medida,medidas_test):
    esTMP = False
    esHUM = False
    esCO = False

    # Segun la medida que me pidan solicitare luego en el JavaScript una medida u otra:
    if medida == 'Temperatura':
        esTMP = True
    elif medida == 'Humedad':
        esHUM = True
    elif medida == 'CO2':
        esCO = True

    info_mota = []  # aqui almacenare solo las que el id de mota coincida con el pedido
    for medidas in medidas_test:    # medidas es cada uno de los diccionarios
        if str(medidas.get("id_mota")) == str(mota):    # comparo id como str sino no reconoce al ser str == int
            info_mota.append(medidas)

    return info_mota

# ------------------------------------------------------------------------------

@csrf_exempt
def slices(request, peticion):
    # Consigo el usuario que ha accedido al portal
    user = request.user
    # Esto es para conseguir saber que slice me estan pidiendo
    url = request.path
    url_slices = url.split('/')[2] # Obtengo slices_ED_70, slices_Clinica_Fuenlabrada y slices_Lece

    # Meto el nombre del edificio para personalizarlo más
    if (url_slices == "slices_ED_70"):
        nombre_ed = "Edificio 70, Ciemat"
    elif (url_slices == "slices_Clinica_Fuenlabrada"):
        nombre_ed = "Clínica de Fuenlabrada"
    elif (url_slices == "slices_Lece"):
        nombre_ed = "Plataforma Solar de Andalucía, Almería"

    # Consigo los datos:
    medidas_test = get_data()

    # Esto me permite mostrar el menú desplegable
    cant_motas = insert_idMota(medidas_test)

    if request.method == 'POST':
        mota_concreta = request.POST['mota']    # Averiguo sobre que mota en concreto solicitan info
        medida_concreta = request.POST['medidatipo']    # Averiguo sobre que medida en concreto solicitan info
        medidas_send = procesolicitud(mota_concreta,medida_concreta,medidas_test)
    else:
        medidas_send = medidas_test # si es un GET mando todas las medidas tal cual las recibo de get_medidas()

    # Llamo a la función que me dirá a que edificios tiene acceso ese usuario
    pages_info_user = users_pages(str(user))

    # Llamo a la funcion que me indica si hay alerta de valores anomalos o no:
    alerta = check_values(medidas_test)

    # Tipos de medidas a elegir:
    meds = ['Temperatura','Humedad','CO2']

    # Lo inroduzco como contexto para representarlo despues
    contexto = {'Builds':pages_info_user, 'User': user,'Medidas': medidas_send, 'alerta':alerta, 'Edificio': nombre_ed, 'Id_motas': cant_motas, 'Tipos_med': meds, 'esTMP': esTMP, 'esHUM': esHUM, 'esCO': esCO}

    return render(request,'slices.html',contexto)

# ------------------------------------------------------------------------------

@csrf_exempt
def tables(request, peticion):
    print(request)
    # Consigo el usuario que ha accedido al portal
    user = request.user
    # usuario = str(user)
    # print("User is: "+usuario)

    # -------- Esto es para conseguir saber que tabla me estan pidiendo ----
    url = request.path
    url_tables = url.split('/')[2] # Obtengo tables_ED_70, tables_Clinica_Fuenlabrada y tables_Lece
    print("Solicitan la tabla: "+url_tables)

    # medidas_test = get_medidas(url_tables) # medidas_test es la lista de diccionarios
    # Consigo los datos:
    medidas_test = get_data()

    # Des de aquiiiiiiiiiii
    # Hasta aquiiiiiii se podria exportar a una funcion introduce id_mota --> ya hecho solo llamo a la funcion
    cant_motas = insert_idMota(medidas_test)


    if request.method == 'POST':
        print(request.POST['mota'])
        mota_concreta = request.POST['mota']    # Averiguo sobre que mota en concreto solicitan info
        # medidas_test = get_medidas(url_tables) # medidas_test es la lista de diccionarios
        info_mota = []  # aqui almacenare solo las que el id de mota coincida con el pedido
        for medidas in medidas_test:    # medidas es cada uno de los diccionarios
            print("La verdadera: "+str(medidas.get("id_mota")))
            if str(medidas.get("id_mota")) == str(mota_concreta):    # comparo id como str sino no reconoce al ser str == int
                info_mota.append(medidas)
        medidas_send = info_mota    # si es un POST mando las medidas de una mota concreta
    else:
        medidas_send = medidas_test # si es un GET mando todas las medidas tal cual las recibo de get_medidas()

    # Llamo a la función que me dirá a que edificios tiene acceso ese usuario
    pages_info_user = users_pages(str(user))

    # Lo inroduzco como contexto para representarlo despues
    contexto = {'Builds':pages_info_user, 'User': user,'Medidas': medidas_send, 'Id_motas': cant_motas}

    return render(request,'tables.html',contexto)

# ------------------------------------------------------------------------------

def leaflet(request, peticion):
    # print(request)  # Esto devuelve <WSGIRequest: GET '/leaflet_ED70.html'>
    # print(request.path) # Esto devuelve /urjc/leaflet_ED70.html

    # -------- Esto es para conseguir saber que leaflet me estan pidiendo ----
    url = request.path
    url_leaflet = url.split('/')[2] # Obtengo leaflet_ED70, leaflet_CF o leaflet_Alm
    print(url_leaflet)

    contexto = {'URL':url_leaflet}
    leaf_plantilla = url_leaflet+'.html'
    # ---------------------------------------------------------------------------------------

    # Consigo el usuario que ha accedido al portal
    user = request.user
    print("User is: "+str(user))

    # Llamo a la función que me dirá a que edificios tiene acceso ese usuario
    pages_info_user = users_pages(str(user))

    # Lo inroduzco como contexto para representarlo despues
    contexto = {'Builds':pages_info_user}

    return render(request,leaf_plantilla,contexto)

# ------------------------------------------------------------------------------

def maps(request,peticion):
    # Consigo el usuario que ha accedido al portal
    user = request.user
    print("User is: "+str(user))

    # Llamo a la función que me dirá a que edificios tiene acceso ese usuario
    pages_info_user = users_pages(str(user))

    # Lo inroduzco como contexto para representarlo despues
    contexto = {'Builds':pages_info_user}

    return render(request,'moving_planos.html',contexto)

# ------------------------------------------------------------------------------

def administration(request,peticion):
    # print(request)  # <WSGIRequest: GET '/urjc/logout'>
    # print(peticion) # urjc
    url = request.path
    url_user = url.split('/')[1] # Obtengo urjc, ciemat o com_mad
    print("El usuario usurpador es: "+url_user)
    if url_user == 'urjc':
        redireccion = '/admin'
    else:
        redireccion = '/'+url_user+'/index'

    return redirect(redireccion)

# ------------------------------------------------------------------------------

def relations(request,peticion):
    # Consigo el usuario que ha accedido al portal
    user = request.user
    print("User is: "+str(user))

    # Llamo a la funcion de test de acceso a sql
    dict = get_CF_info()

    # Llamo a la función que me dirá a que edificios tiene acceso ese usuario
    pages_info_user = users_pages(str(user))

    # Lo inroduzco como contexto para representarlo despues
    contexto = {'Builds':pages_info_user, 'User': user, 'Dict': dict}

    return render(request,'relations.html',contexto)
