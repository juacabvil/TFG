# Sevidis: una aplicación multi-plataforma para la ayuda de personas con discapacidad en Sevilla

![image](https://github.com/juacabvil/TFG/assets/73932871/ef2cdae2-c397-4909-a625-ccde9a4a1ace)


## Descripción del proyecto

El proyecto de Sevidis es un **Trabajo de Final de Grado** de **Ingeniería Informática** orientado a la construcción de una aplicación multi-plataforma destinada a la ayuda de personas con discapacidad en la provincia de Sevilla, concretamente, 
en esta primera versión a las personas de la capital. 

La plataforma cuenta con un **mapa** con información sobre la **accesibilidad** de **345 establecimientos** y **140 aparcamientos** iniciales situados a **12 km** a la redonda desde un punto céntrico de la ciudad. 
Además también se incluye una funcionalidad de **cálculo de rutas** aprovechando que en Sevilla es posible desplazarse en silla de ruedas a través de carriles bici, 
incluyendo también una función que traza rutas en coche teniendo en cuenta los aparcamientos reservados cercanos para personas con baja movilidad. 

En adición, se incluye un sistema de **integración de nuevos puntos**, **reseñas** a los ya existentes y un **manual completo** con información sobre el funcionamiento de la plataforma, 
además de **lectura de botones y textos** para personas con problemas de visión en una interfaz amigable y responsiva.

## Herramientas utilizadas

El proyecto integra funcionalidades de las siguientes herramientas:

- Leaflet: una librería JavaScript para crear mapas interactivos.
- Open Street Maps: un proyecto colaborativo para crear mapas libres y editables.
- GraphHopper: un servicio web para calcular rutas óptimas entre puntos.
- Overpass Turbo: una herramienta para consultar datos geográficos de Open Street Maps.
- Responsive Voice: una librería JavaScript para generar voz sintética.
- Bootstrap: un framework CSS para diseñar sitios web responsivos y adaptables.
- Leaflet Extra Markers: una extensión de Leaflet para añadir marcadores personalizados.

# ¿Como arrancar?

## Con python 3.10 en Windows o Linux:

### Entorno virtual

- python -m venv .	(Para crear un entorno virtual en el directorio local)

- .\Scripts\activate.bat	(En Windows, para arrancar el entorno virtual)

- source venv/bin/activate (En Linux, para arrancar el entorno virtual)

### Dependencias y arranque

- pip install  -r  .\requirements.txt	(Usamos el comando para descargar las dependencias)

- python.exe .\manage.py runserver	(Para arrancar la aplicación localmente)

## Con Docker:

- docker pull juacabvil/sevidis:1.0.0

- docker run -p 8000:8000 juacabvil/sevidis:1.0.0

Acceder a localhost:8000

## Créditos

Este proyecto no es propietario ni responsable del contenido o funcionamiento de las herramientas mencionadas anteriormente. Todos los créditos y derechos pertenecen a sus respectivos autores.
