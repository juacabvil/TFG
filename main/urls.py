from django.urls import path
from main import views

urlpatterns = [
    path("", views.home, name="home"),
    path("buscas", views.buscas,name="buscas"),
    path("mapa", views.mapa,name="mapa"),
]