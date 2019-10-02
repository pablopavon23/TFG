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
# Importamos el archivo y función que reside en el mismo para cargar medidas:
from .load_medidas import get_medidas, test_sql;

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
        contexto = {'Login':"Hola"}
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
    contexto = {'Registro':"Hola"}
    return render(request,'register.html',contexto)
    # return HttpResponse("Hello people")

# ------------------------------------------------------------------------------

@csrf_exempt
def index(request, peticion):
    # Consigo el usuario que ha accedido al portal
    user = request.user
    print("User is: "+str(user))

    # Llamo a la funcion de test de acceso a sql
    test_medidas = test_sql()
    test_motas = test_medidas[0].id_mota
    test_sensores = test_medidas[0].num_sensores

    # Llamo a la función que me dirá a que edificios tiene acceso ese usuario
    pages_info_user = users_pages(str(user))

    # Lo inroduzco como contexto para representarlo despues
    contexto = {'Builds':pages_info_user, 'User': user, 'Medidas_mota': test_motas, 'Medidas_sensores': test_sensores}

    return render(request,'index.html',contexto)

# ------------------------------------------------------------------------------

def check_values(medidas_test):
    # Comprobamos que no haya valores anómalos en temperaturas: ----------------
    temperaturas = []
    for medidas in medidas_test:    # medidas es cada uno de los diccionarios
        print("La temperatura: "+str(medidas.get("TMPaire")))
        if ((medidas.get("TMPaire")) != None):   # Si no tenemos medida no se añade
            temperaturas.append(medidas.get("TMPaire"))

    print("Temperaturas: "+str(temperaturas))
    temperaturas = sorted(temperaturas)
    print("Las motas despues son: "+str(temperaturas))    # Agrupamos los temperatura en orden ascendente

    if (temperaturas[0] < 0.0) or (temperaturas[len(temperaturas)-1] > 50.0):
        alertar_TMP = True
    else:
        alertar_TMP = False
    # --------------------------------------------------------------------------

    # Comprobamos que no haya valores anómalos en co2: ----------------
    dioxido = []
    for medidas in medidas_test:    # medidas es cada uno de los diccionarios
        if ((medidas.get("CO2")) != None):   # Si no tenemos medida no se añade
            dioxido.append(medidas.get("CO2"))

    print("c02: "+str(dioxido))
    dioxido = sorted(dioxido)
    print("c02 despues son: "+str(dioxido))    # Agrupamos los temperatura en orden ascendente

    if (dioxido[0] < 0.0) or (dioxido[len(dioxido)-1] > 810.0):
        alertar_CO = True
    else:
        alertar_CO = False
    # --------------------------------------------------------------------------

    # Comprobamos que no haya valores anómalos en humedades: ----------------
    humedades = []
    for medidas in medidas_test:    # medidas es cada uno de los diccionarios
        if ((medidas.get("HUMEDAD")) != None):   # Si no tenemos medida no se añade
            humedades.append(medidas.get("HUMEDAD"))

    print("humedades: "+str(humedades))
    humedades = sorted(humedades)
    print("humedades despues son: "+str(humedades))    # Agrupamos los temperatura en orden ascendente

    if (humedades[0] < 0.0) or (humedades[len(humedades)-1] > 85.0):
        alertar_HU = True
    else:
        alertar_HU = False
    # --------------------------------------------------------------------------

    if (not alertar_TMP) and (not alertar_CO) and (not alertar_HU):
        alertar = False
    else:
        alertar = True

    """ La función de esta función es devolver si hay que alertar o no"""
    return alertar

# ------------------------------------------------------------------------------

@csrf_exempt
def slices(request, peticion):
    # Consigo el usuario que ha accedido al portal
    user = request.user
    print("User is: "+str(user))

    # -------- Esto es para conseguir saber que slice me estan pidiendo ----
    url = request.path
    url_slices = url.split('/')[2] # Obtengo slices_ED_70, slices_Clinica_Fuenlabrada y slices_Lece
    print(url_slices)

    # -------- Esto es para conseguir saber que slice me estan pidiendo ----
    url = request.path
    url_slices = url.split('/')[2] # Obtengo slices_ED_70, slices_Clinica_Fuenlabrada y slices_Lece
    print("Solicitan la slice: "+url_slices)
    # Meto el nombre del edificio para personalizarlo más
    if (url_slices == "slices_ED_70"):
        nombre_ed = "Edificio 70, Ciemat"
    elif (url_slices == "slices_Clinica_Fuenlabrada"):
        nombre_ed = "Clínica de Fuenlabrada"
    elif (url_slices == "slices_Lece"):
        nombre_ed = "Plataforma Solar de Andalucía, Almería"

    medidas_test = get_medidas(url_slices) # medidas_test es la lista de diccionarios
    # La funcion get_medidas me devuelve la lista con las medidas para un edificio concreto

# --------- Copio tal cual de tables
    cant_motas = []   # Inicializo la lista donde guardare mota1, mota2...
    for medidas in medidas_test:    # medidas es cada uno de los diccionarios
        id_mota = medidas.get("mota")  # esto me permite saber que id de mota tengo
        print("Mota: "+str(id_mota)) #ASi obtengo la mota a la que pertenece
        if not str(id_mota) in cant_motas:
            cant_motas.append(str(id_mota))

    print("El numero de motas es: "+str(len(cant_motas)))
    cant_motas = sorted(cant_motas)
    print("Las motas despues son: "+str(cant_motas))    # Agrupamos los id_mota en orden ascendente
    # Hasta aquiiiiiii se podria exportar a una funcion introduce id_mota

    esTMP = False
    esHUM = False
    esCO = False
    if request.method == 'POST':
        mota_concreta = request.POST['mota']    # Averiguo sobre que mota en concreto solicitan info
        print("La mota es: "+mota_concreta)
        medida_concreta = request.POST['medidatipo']    # Averiguo sobre que medida en concreto solicitan info
        print("La medida es: "+medida_concreta)
        # Segun la medida que me pidan solicitare luego en el JavaScript una medida u otra:
        if medida_concreta == 'Temperatura':
            esTMP = True
        elif medida_concreta == 'Humedad':
            esHUM = True
        elif medida_concreta == 'CO2':
            esCO = True
        info_mota = []  # aqui almacenare solo las que el id de mota coincida con el pedido
        for medidas in medidas_test:    # medidas es cada uno de los diccionarios
            print("La verdadera: "+str(medidas.get("mota")))
            if str(medidas.get("mota")) == str(mota_concreta):    # comparo id como str sino no reconoce al ser str == int
                info_mota.append(medidas)
        medidas_send = info_mota    # si es un POST mando las medidas de una mota concreta
    else:
        medidas_send = medidas_test # si es un GET mando todas las medidas tal cual las recibo de get_medidas()
# -- Hasta aqui copio tal cual de tables

    # Llamo a la función que me dirá a que edificios tiene acceso ese usuario
    pages_info_user = users_pages(str(user))

    # Llamo a la funcion que me indica si hay alerta de valores anomalos o no:
    alerta = check_values(medidas_test)

    # Tipos de medidas a elegir:
    meds = ['Temperatura','Humedad','CO2']

    # Lo inroduzco como contexto para representarlo despues
    contexto = {'Builds':pages_info_user, 'Medidas': medidas_send, 'alerta':alerta, 'Edificio': nombre_ed, 'Id_motas': cant_motas, 'Tipos_med': meds, 'esTMP': esTMP, 'esHUM': esHUM, 'esCO': esCO}

    return render(request,'slices.html',contexto)

# ------------------------------------------------------------------------------

@csrf_exempt
def tables(request, peticion):
    print(request)
    # Consigo el usuario que ha accedido al portal
    user = request.user
    usuario = str(user)
    print("User is: "+usuario)

    # -------- Esto es para conseguir saber que tabla me estan pidiendo ----
    url = request.path
    url_tables = url.split('/')[2] # Obtengo tables_ED_70, tables_Clinica_Fuenlabrada y tables_Lece
    print("Solicitan la tabla: "+url_tables)
    medidas_test = get_medidas(url_tables) # medidas_test es la lista de diccionarios

    # Des de aquiiiiiiiiiii
    cant_motas = []   # Inicializo la lista donde guardare mota1, mota2...
    for medidas in medidas_test:    # medidas es cada uno de los diccionarios
        id_mota = medidas.get("mota")  # esto me permite saber que id de mota tengo
        print("Mota: "+str(id_mota)) #ASi obtengo la mota a la que pertenece
        if not str(id_mota) in cant_motas:
            cant_motas.append(str(id_mota))

    print("El numero de motas es: "+str(len(cant_motas)))
    cant_motas = sorted(cant_motas)
    print("Las motas despues son: "+str(cant_motas))    # Agrupamos los id_mota en orden ascendente
    # Hasta aquiiiiiii se podria exportar a una funcion introduce id_mota

    if request.method == 'POST':
        print(request.POST['mota'])
        mota_concreta = request.POST['mota']    # Averiguo sobre que mota en concreto solicitan info
        # medidas_test = get_medidas(url_tables) # medidas_test es la lista de diccionarios
        info_mota = []  # aqui almacenare solo las que el id de mota coincida con el pedido
        for medidas in medidas_test:    # medidas es cada uno de los diccionarios
            print("La verdadera: "+str(medidas.get("mota")))
            if str(medidas.get("mota")) == str(mota_concreta):    # comparo id como str sino no reconoce al ser str == int
                info_mota.append(medidas)
        medidas_send = info_mota    # si es un POST mando las medidas de una mota concreta
    else:
        medidas_send = medidas_test # si es un GET mando todas las medidas tal cual las recibo de get_medidas()

    # Llamo a la función que me dirá a que edificios tiene acceso ese usuario
    pages_info_user = users_pages(str(user))

    # Lo inroduzco como contexto para representarlo despues
    contexto = {'Builds':pages_info_user, 'Medidas': medidas_send, 'Id_motas': cant_motas}

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
