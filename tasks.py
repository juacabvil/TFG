# tasks.py

from django.conf import settings
import requests
import xml.etree.ElementTree as ET
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sevidis.settings")

import django
django.setup()

from main.models import PuntoDeInteres, Aparcamiento

def guardar_aparcamientos():
    print('Comienzo de guardado de aparcamientos') 
    kml_file_path = 'main/static/files/Estacionamientos.kml'
    tree = ET.parse(kml_file_path)
    root = tree.getroot()

    coordenadas_procesadas = set()

    aparcamientos = []
    for placemark in root.findall('.//{http://www.opengis.net/kml/2.2}Placemark'):
        name = placemark.find('{http://www.opengis.net/kml/2.2}name').text
        description = placemark.find(
            '{http://www.opengis.net/kml/2.2}description').text
        coordinates = placemark.find(
            './/{http://www.opengis.net/kml/2.2}coordinates').text

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
        existing_aparcamiento = Aparcamiento.objects.filter(
            latitud=aparcamiento_data['latitud'],
            longitud=aparcamiento_data['longitud']
        ).first()

        if existing_aparcamiento:
            existing_aparcamiento.nombre = aparcamiento_data['nombre']
            existing_aparcamiento.descripcion = aparcamiento_data['descripcion']
            existing_aparcamiento.save()
        else:
            aparcamiento = Aparcamiento(
                nombre=aparcamiento_data['nombre'],
                descripcion=aparcamiento_data['descripcion'],
                latitud=aparcamiento_data['latitud'],
                longitud=aparcamiento_data['longitud'],
            )
            aparcamiento.save()
    print('Completado guardado de aparcamientos')        

def guardar_puntos_de_interes():
    print('Comienza guardado de puntos de interés')
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

            existing_poi = PuntoDeInteres.objects.filter(
                latitud=element['lat'], longitud=element['lon']).first()

            if existing_poi:
                existing_poi.nombre = element.get(
                    'tags', {}).get('name', 'Sin nombre')
                existing_poi.descripcion = element.get(
                    'tags', {}).get('description', '')
                existing_poi.tipo_amenidad = element.get(
                    'tags', {}).get('amenity', 'Desconocido')
                existing_poi.datos_adicionales = datos_adicionales
                existing_poi.accesibilidad = element.get(
                    'tags', {}).get('wheelchair', 'no')
                existing_poi.save()
            else:
                PuntoDeInteres.objects.create(
                    latitud=element['lat'],
                    longitud=element['lon'],
                    nombre=element.get('tags', {}).get('name', 'Sin nombre'),
                    descripcion=element.get('tags', {}).get('description', ''),
                    tipo_amenidad=element.get('tags', {}).get(
                        'amenity', 'Desconocido'),
                    datos_adicionales=datos_adicionales,
                    accesibilidad=element.get(
                        'tags', {}).get('wheelchair', 'no')
                )
    print('Completado guardado de puntos de interés')

if __name__ == "__main__":
    guardar_aparcamientos()
    guardar_puntos_de_interes()


