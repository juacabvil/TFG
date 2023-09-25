from django.urls import path, include
from main import views


urlpatterns = [
    path("", views.home, name="home"),
    path("buscas", views.buscas,name="buscas"),
    path("mapa", views.mapa,name="mapa"),
    path("inicio_sesion", views.InicioSesionView.as_view(),name="inicio_sesion"),
    path("registro", views.RegistroView.as_view(),name="registro"),
    path('logout', views.logout_view, name='logout'),
    path('nuevo_punto', views.NuevoPuntoView.as_view(), name='nuevo_punto'),
    path('eliminar_punto', views.EliminarPuntoUsuarioView.as_view(), name='eliminar_punto'),
    path('procesar_opinion/', views.procesar_opinion, name='procesar_opinion'),
    path('informacion', views.informacion, name='informacion'),
    path('gdpr', views.gdpr, name='gdpr'),
    path('', include('pwa.urls')),
    
    
]