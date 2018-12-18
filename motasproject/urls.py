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
from motas import views
from motasproject import settings

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'motas.views.user_login'),
    url(r'^register', 'motas.views.register'),
    url(r'^(.*)/index', 'motas.views.index'),
    url(r'^(.*)/slices', 'motas.views.slices'),
    url(r'^(.*)/tables', 'motas.views.tables'),
    url(r'^(.*)/leaflet_ED70', 'motas.views.leaflet'),
    url(r'^(.*)/leaflet_CF', 'motas.views.leaflet'),
    url(r'^(.*)/leaflet_Alm', 'motas.views.leaflet'),
    url(r'^(.*)/maps', 'motas.views.maps'),
]

"""
import motas.views as motas_views

    url(r'^change.css/', aparca_views.personalizar, name='Personalizar css'),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_URL}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', aparca_views.pagina_principal, name='Página principal'),
    url(r'^login' , aparca_views.loginuser, name='Loguearse'),
    url(r'^logout', aparca_views.mylogout, name='Logout'),
    url(r'^aparcamientos/$', aparca_views.aparcamientos, name='Aparcamientos'),
    url(r'^aparcamientos/(.*)', aparca_views.aparcamientos_id, name='Aparcamiento concreto'),
    url(r'^about/', aparca_views.about, name='Ayuda'),
    url(r'^(.*)/xml/', aparca_views.usuarios_xml, name='Pagina XML de un usuario'),
    url(r'^(.*)/$', aparca_views.usuarios, name='Pagina personal de un usuario'),
"""
