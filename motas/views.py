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
from .load_medidas import get_medidas;

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

    # Llamo a la función que me dirá a que edificios tiene acceso ese usuario
    pages_info_user = users_pages(str(user))

    # Lo inroduzco como contexto para representarlo despues
    contexto = {'Builds':pages_info_user, 'User': user}

    return render(request,'index.html',contexto)

# ------------------------------------------------------------------------------

def slices(request, peticion):
    # Consigo el usuario que ha accedido al portal
    user = request.user
    print("User is: "+str(user))

    # -------- Esto es para conseguir saber que slice me estan pidiendo ----
    url = request.path
    url_slices = url.split('/')[2] # Obtengo slices_ED_70, slices_Clinica_Fuenlabrada y slices_Lece
    print(url_slices)

    # Begin Test Highcharts --------------------------->
    dataset_1 = [
      {'ticket_class': 1, 'survived_count': 200, 'not_survived_count': 123},
      {'ticket_class': 2, 'survived_count': 119, 'not_survived_count': 158},
      {'ticket_class': 3, 'survived_count': 181, 'not_survived_count': 528}
    ]
    dataset_2 = [
      {'ticket_class': 3, 'survived_count': 300, 'not_survived_count': 223},
      {'ticket_class': 4, 'survived_count': 219, 'not_survived_count': 258},
      {'ticket_class': 5, 'survived_count': 281, 'not_survived_count': 628}
    ]
    dataset_3 = [
      {'ticket_class': 6, 'survived_count': 400, 'not_survived_count': 323},
      {'ticket_class': 7, 'survived_count': 319, 'not_survived_count': 358},
      {'ticket_class': 8, 'survived_count': 381, 'not_survived_count': 728}
    ]

    diccionario = {
    'Test_1': dataset_1,
    'Test_2': dataset_2,
    'Test_3': dataset_3
    }

    # En función de la solicitud de gráfica realizada proceso una base de datos de medidas u otra
    # # PEROOOJO que ahora mismo solo estoy testeando aunque la estructura del if me valdrá luego
    if url_slices == 'slices_ED_70':
        dataset = diccionario.get('Test_1')
    elif url_slices == 'slices_Clinica_Fuenlabrada':
        dataset = diccionario.get('Test_2')
    elif url_slices == 'slices_Lece':
        dataset = diccionario.get('Test_3')
    # End Test Highcharts --------------------------->

    # Llamo a la función que me dirá a que edificios tiene acceso ese usuario
    pages_info_user = users_pages(str(user))

    # Lo inroduzco como contexto para representarlo despues
    contexto = {'Builds':pages_info_user, 'dataset':dataset}

    return render(request,'slices_test.html',contexto)

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
    contexto = {'Medidas': medidas_send, 'Id_motas': cant_motas}

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
