from django.urls import path
from main import views

urlpatterns = [
    path("", views.home, name="home"),
    path("buscas", views.buscas,name="buscas"),
    path("mapa", views.mapa,name="mapa"),
    path("inicio_sesion", views.InicioSesionView.as_view(),name="inicio_sesion"),
    path("registro", views.RegistroView.as_view(),name="registro"),
    path('logout', views.logout_view, name='logout'),
    path('cargar_puntos', views.guardar_puntos_de_interes, name='cargar_puntos'),
     path('aparcamientos', views.guardar_aparcamientos, name='aparcamientos'),
    
    
]