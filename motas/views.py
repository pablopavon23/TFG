from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template

# Create your views here.
def login(request):
    contexto = Context({'Login':"Hola"})
    return render(request,'login.html',contexto)
    # return HttpResponse("Hello people")

def register(request):
    contexto = Context({'Registro':"Hola"})
    return render(request,'register.html',contexto)
    # return HttpResponse("Hello people")

def index(request):
    contexto = Context({'Indice':"Hola"})
    return render(request,'index.html',contexto)
    # return HttpResponse("Hello people")

def forgot_password(request):
    contexto = Context({'Olvidado':"Hola"})
    return render(request,'forgot-password.html',contexto)
    # return HttpResponse("Hello people")

def charts(request):
    contexto = Context({'Graficos':"Hola"})
    return render(request,'charts.html',contexto)
    # return HttpResponse("Hello people")

def tables(request):
    contexto = Context({'TablasDatos':"Hola"})
    return render(request,'tables.html',contexto)
    # return HttpResponse("Hello people")

def leaflet(request):
    contexto = Context({'Mapas':"Hola"})
    return render(request,'leaflet_ED70.html',contexto)
    # return HttpResponse("Hello people")

def maps(request):
    contexto = Context({'Mapas2':"Hola"})
    return render(request,'maps.html',contexto)
    # return HttpResponse("Hello people")
