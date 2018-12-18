"""motasproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from motasproject import settings
import motas.views as motas_views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', motas_views.user_login, name='Login'),
    url(r'^register', motas_views.register, name='Registrarse'),
    url(r'^(.*)/index', motas_views.index, name='Página principal'),
    url(r'^(.*)/logout', motas_views.user_logout, name='Logout'),
    url(r'^(.*)/slices', motas_views.slices, name='Graficas'),
    url(r'^(.*)/tables', motas_views.tables, name='Datos'),
    url(r'^(.*)/leaflet', motas_views.leaflet, name='Leaflet'),
    url(r'^(.*)/maps', motas_views.maps, name='Mapas'),
]
