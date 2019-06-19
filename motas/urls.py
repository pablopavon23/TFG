from django.urls import path
from django.conf.urls import url

# from . import views
import motas.views as motas_views

urlpatterns = [
    # ex: localhost:1234/
    url(r'^$', motas_views.user_login),
    # ex: localhost:1234/register
    url(r'^register$', motas_views.register),
    # ex: localhost:1234/(entidad)/index
    url(r'^(.*)/index', motas_views.index),
    # ex: localhost:1234/(entidad)/logout
    url(r'^(.*)/logout', motas_views.user_logout),
    # ex: localhost:1234/(entidad)/slices
    url(r'^(.*)/slices', motas_views.slices),
    # ex: localhost:1234/(entidad)/tables
    url(r'^(.*)/tables', motas_views.tables),
    # ex: localhost:1234/(entidad)/leaflet
    url(r'^(.*)/leaflet', motas_views.leaflet),
    # ex: localhost:1234/(entidad)/maps
    url(r'^(.*)/maps', motas_views.maps),
    # ex: localhost:1234/(entidad)/administration
    url(r'^(.*)/administration', motas_views.administration),
]
