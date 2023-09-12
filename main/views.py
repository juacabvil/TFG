from django.shortcuts import render, redirect  
from django.contrib.auth import login, authenticate, logout
from django.views import View
from .forms import RegistroForm, InicioSesionForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import PuntoDeInteres, Aparcamiento
import requests
import xml.etree.ElementTree as ET
from django.conf import settings

def home(request):
    return render(
        request,
        'main/landing.html',
    )
def buscas(request):
    return render(
        request,
        'main/buscas.html',
    )
def mapa(request):
    puntos_de_interes = PuntoDeInteres.objects.all()
    aparcamientos = Aparcamiento.objects.all()
    
    puntos_interes_para_mapa = []
    aparcamientos_para_mapa = []
    
    for punto in puntos_de_interes:
        latitud = punto.latitud
        longitud = punto.longitud
        nombre = punto.nombre
        descripcion = punto.descripcion
        datos_adicionales = punto.datos_adicionales
        color = punto.get_marker_color() 
        icono = punto.get_marker_icon()

        popup_content = f"<h2>{nombre}</h2>"
        popup_content += f"<p>{descripcion}</p>"

        if datos_adicionales:
            for clave, valor in datos_adicionales.items():
                popup_content += f"<p><strong>{clave}:</strong> {valor}</p>"

        marcador = {
            'latitud': latitud,
            'longitud': longitud,
            'popup_content': popup_content,
            'color':color,
            'icono':icono
            
        }

        puntos_interes_para_mapa.append(marcador)

    for aparcamiento in aparcamientos:
        latitud = aparcamiento.latitud
        longitud = aparcamiento.longitud
        nombre = aparcamiento.nombre
        descripcion = aparcamiento.descripcion

        popup_content = f"<h2>{nombre}</h2>"
        popup_content += f"<p>{descripcion}</p>"

        marcador = {
            'latitud': latitud,
            'longitud': longitud,
            'popup_content': popup_content
        }

        aparcamientos_para_mapa.append(marcador)

    return render(
        request,
        'main/mapa.html',
        {'puntos_interes_para_mapa': puntos_interes_para_mapa, 'aparcamientos_para_mapa': aparcamientos_para_mapa}
    )

def logout_view(request):
    logout(request)
    return redirect('home')

def guardar_aparcamientos(request):
    Aparcamiento.objects.all().delete()
    kml_file_path = settings.STATIC_ROOT + '\\files\\Estacionamientos.kml'
    tree = ET.parse(kml_file_path)
    root = tree.getroot()

    coordenadas_procesadas = set()

    aparcamientos = []
    for placemark in root.findall('.//{http://www.opengis.net/kml/2.2}Placemark'):
        name = placemark.find('{http://www.opengis.net/kml/2.2}name').text
        description = placemark.find('{http://www.opengis.net/kml/2.2}description').text
        coordinates = placemark.find('.//{http://www.opengis.net/kml/2.2}coordinates').text

        coordinates = coordinates.split(',')
        longitude, latitude, _ = map(float, coordinates)

        if (latitude, longitude) in coordenadas_procesadas:
            continue  

        coordenadas_procesadas.add((latitude, longitude))

        aparcamientos.append({
            'nombre': name,
            'descripcion': description,
            'latitud': latitude,
            'longitud': longitude,
        })

    for aparcamiento_data in aparcamientos:
        aparcamiento = Aparcamiento(
            nombre=aparcamiento_data['nombre'],
            descripcion=aparcamiento_data['descripcion'],
            latitud=aparcamiento_data['latitud'],
            longitud=aparcamiento_data['longitud'],
        )
        aparcamiento.save()

    return redirect('home')


def guardar_puntos_de_interes(request):
    PuntoDeInteres.objects.all().delete()
    overpass_url = 'https://overpass-api.de/api/interpreter'
    overpass_query = """
        [out:json];
        (
            node["amenity"]["wheelchair"](around:12000,37.35880525026899,-5.987216388358271);
            way["amenity"]["wheelchair"](around:12000,37.35880525026899,-5.987216388358271);
        );
        out center;
    """

    response = requests.post(overpass_url, data={'data': overpass_query})
    data = response.json()

    for element in data.get('elements', []):
        if 'lat' in element and 'lon' in element:
            
            datos_adicionales = {}

            for key, value in element.get('tags', {}).items():
                datos_adicionales[key] = value
                
            
            PuntoDeInteres.objects.create(
                latitud=element['lat'],
                longitud=element['lon'],
                nombre=element.get('tags', {}).get('name', 'Sin nombre'),
                descripcion=element.get('tags', {}).get('description', ''),
                tipo_amenidad=element.get('tags', {}).get('amenity', 'Desconocido'),
                datos_adicionales=datos_adicionales,
                accesibilidad=element.get('tags', {}).get('wheelchair', 'no'),  
            )
            
             
    return redirect('home')

            

class RegistroView(View):
    def get(self, request):
        form = RegistroForm()
        return render(request, 'main/registro.html', {'form': form})

    def post(self, request):
        form = RegistroForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(request=request)  
            return redirect('mapa')
        return render(request, 'main/registro.html', {'form': form})


class InicioSesionView(View):
    def get(self, request):
        form = InicioSesionForm()
        return render(request, 'main/inicio_sesion.html', {'form': form})

    def post(self, request):
        form = InicioSesionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('mapa')
        return render(request, 'main/inicio_sesion.html', {'form': form})

