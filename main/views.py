from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from .forms import RegistroForm, InicioSesionForm
from .models import PuntoDeInteres, Aparcamiento, PuntoUsuario, Opinion
import requests
import xml.etree.ElementTree as ET
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404


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

def informacion(request):
    return render(
        request,
        'main/informacion.html',
    )
    
def gdpr(request):
    return render(
        request,
        'main/gdpr.html',
    )
def mapa(request):
    puntos_de_interes = PuntoDeInteres.objects.all()
    aparcamientos = Aparcamiento.objects.all()
    puntos_usuario = PuntoUsuario.objects.all()

    puntos_interes_para_mapa = []
    aparcamientos_para_mapa = []
    puntos_usuario_para_mapa = []

    for punto in puntos_de_interes:
        id = punto.id
        latitud = punto.latitud
        longitud = punto.longitud
        nombre = punto.nombre
        descripcion = punto.descripcion
        datos_adicionales = punto.datos_adicionales
        color = punto.get_marker_color()
        icono = punto.get_marker_icon()
        opiniones = Opinion.objects.filter(punto_interes=punto)
        texto_opiniones = [opinion.texto for opinion in opiniones]

        popup_content = f"<h2>{nombre}</h2>"
        popup_content += f"<p>{descripcion}</p>"

        if datos_adicionales:
            for clave, valor in datos_adicionales.items():
                popup_content += f"<p><strong>{clave}:</strong> {valor}</p>"

        marcador = {
            'nombre':nombre,
            'id': id,
            'latitud': latitud,
            'longitud': longitud,
            'popup_content': popup_content,
            'color': color,
            'icono': icono,
            'opiniones': texto_opiniones,

        }

        puntos_interes_para_mapa.append(marcador)

    for aparcamiento in aparcamientos:
        id = aparcamiento.id
        latitud = aparcamiento.latitud
        longitud = aparcamiento.longitud
        nombre = aparcamiento.nombre
        descripcion = aparcamiento.descripcion
        opiniones = Opinion.objects.filter(aparcamiento=aparcamiento)
        texto_opiniones = [opinion.texto for opinion in opiniones]

        popup_content = f"<h2>{nombre}</h2>"
        popup_content += f"<p>{descripcion}</p>"

        marcador = {
            'nombre':nombre,
            'id': id,
            'latitud': latitud,
            'longitud': longitud,
            'popup_content': popup_content,
            'opiniones': texto_opiniones,
        }

        aparcamientos_para_mapa.append(marcador)

    for punto in puntos_usuario:
        id = punto.id
        user = punto.user.id
        latitud = punto.latitud
        longitud = punto.longitud
        nombre = punto.nombre
        descripcion = punto.descripcion
        wc_adaptado = punto.wcAdaptado
        animales_guia = punto.AnimalesGuia
        asistencia = punto.Asistencia
        color = punto.color_accesibilidad
        icono = punto.get_marker_icon()
        opiniones = Opinion.objects.filter(punto_usuario=punto)
        texto_opiniones = [opinion.texto for opinion in opiniones]

        popup_content = f"<h2 class='mb-3'>{nombre}</h2>"
        popup_content += f"<p class='mb-3'>{descripcion}</p>"

        popup_content += "<ul class='list-group'>"
        popup_content += f"<li class='list-group-item'>🚾Baño Adaptado: <span class='badge badge-{ 'success' if wc_adaptado else 'danger' }'>{ 'Si ✅' if wc_adaptado else 'No ⛔' }</span></li>"
        popup_content += f"<li class='list-group-item'>👩‍🦯Animales de Guía: <span class='badge badge-{ 'success' if animales_guia else 'danger' }'>{ 'Si ✅' if animales_guia else 'No ⛔' }</span></li>"
        popup_content += f"<li class='list-group-item'>♿Asistencia: <span class='badge badge-{ 'success' if asistencia else 'danger' }'>{ 'Si ✅' if asistencia else 'No ⛔' }</span></li>"
        popup_content += "</ul>"

        marcador = {
            'nombre':nombre,
            'id': id,
            'latitud': latitud,
            'longitud': longitud,
            'popup_content': popup_content,
            'color': color,
            'icono': icono,
            'opiniones': texto_opiniones,
            'user': user

        }

        puntos_usuario_para_mapa.append(marcador)

    return render(
        request,
        'main/mapa.html',
        {'puntos_interes_para_mapa': puntos_interes_para_mapa,
         'aparcamientos_para_mapa': aparcamientos_para_mapa,
         'puntos_usuario_para_mapa': puntos_usuario_para_mapa,
         'user_is_authenticated': request.user.is_authenticated}
    )


def logout_view(request):
    logout(request)
    return redirect('home')




@csrf_exempt
def procesar_opinion(request):
    if request.method == 'POST':
        texto_opinion = request.POST.get('texto_opinion')
        usuario = request.user
        punto_id = request.POST.get('punto_id')
        punto_tipo = request.POST.get('punto_tipo')

        if not usuario.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'Debes iniciar sesión para enviar una opinión'})

        if not texto_opinion.strip():
            return JsonResponse({'status': 'error', 'message': 'El texto de la opinión no puede estar en blanco'})

        try:
            if punto_tipo == 'punto_de_interes':
                punto = PuntoDeInteres.objects.get(pk=punto_id)
                existing_opinion = Opinion.objects.filter(
                    usuario=usuario, punto_interes=punto).first()
                if existing_opinion:
                    existing_opinion.texto = texto_opinion
                    existing_opinion.save()
                else:
                    Opinion.objects.create(
                        usuario=usuario, texto=texto_opinion, punto_interes=punto)
            elif punto_tipo == 'punto_usuario':
                punto = PuntoUsuario.objects.get(pk=punto_id)
                existing_opinion = Opinion.objects.filter(
                    usuario=usuario, punto_usuario=punto).first()
                if existing_opinion:
                    existing_opinion.texto = texto_opinion
                    existing_opinion.save()
                else:
                    Opinion.objects.create(
                        usuario=usuario, texto=texto_opinion, punto_usuario=punto)

            elif punto_tipo == 'aparcamiento':
                punto = Aparcamiento.objects.get(pk=punto_id)
                existing_opinion = Opinion.objects.filter(
                    usuario=usuario, aparcamiento=punto).first()
                if existing_opinion:
                    existing_opinion.texto = texto_opinion
                    existing_opinion.save()
                else:
                    Opinion.objects.create(
                        usuario=usuario, texto=texto_opinion, aparcamiento=punto)

            else:
                return JsonResponse({'status': 'error', 'message': 'Tipo de punto no válido'})

            return JsonResponse({'status': 'success', 'message': 'Opinión agregada con éxito'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Método no permitido'})


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
                next = request.GET.get('next')
                if next:
                    return redirect(next)
                else:
                    return redirect('mapa')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos')
        else:
            messages.error(
                request, 'Hubo un problema con los datos que ingresaste. Por favor, verifica tus datos.')
        return render(request, 'main/inicio_sesion.html', {'form': form})


class NuevoPuntoView(LoginRequiredMixin, View):
    login_url = 'inicio_sesion'

    def get(self, request):
        latitud = request.GET.get('latitud')
        longitud = request.GET.get('longitud')
        existing_point = PuntoUsuario.objects.filter(
            latitud=latitud, longitud=longitud).first()

        if existing_point:
            if existing_point.user != request.user:
                raise Http404
            return render(request, 'main/nuevo_punto.html', {'punto': existing_point})
        else:
            return render(request, 'main/nuevo_punto.html')

    def post(self, request):
        nombre = request.POST.get('nombre', '')
        descripcion = request.POST.get('descripcion', '')
        amenidad = request.POST.get('amenidad', '')
        color_accesibilidad = request.POST.get('color_accesibilidad', '')
        wc_adaptado = 'wcAdaptado' in request.POST
        animales_guia = 'AnimalesGuia' in request.POST
        asistencia = 'Asistencia' in request.POST
        latitud = request.GET.get('latitud')
        longitud = request.GET.get('longitud')
        errors = []
        

        if not nombre:
            errors.append('El nombre es obligatorio')
       
        if len(nombre) > 100:
            errors.append(f'El nombre no puede tener más de 100 caracteres')
        if len(descripcion) > 2000:
            errors.append(
                f'La descripción no puede tener más de 2000 caracteres')

        if amenidad not in [choice[0] for choice in PuntoUsuario.CATEGORIAS_AMENIDAD_CHOICES]:
            errors.append('Categoría de amenidad no válida')
        if color_accesibilidad not in [choice[0] for choice in PuntoUsuario.COLOR_CHOICES]:
            errors.append('Nivel de accesibilidad no válido')
        try:
            latitud = float(latitud)
            longitud = float(longitud)
            if not (-90 <= latitud <= 90) or not (-180 <= longitud <= 180):
                errors.append(
                    'Latitud y longitud deben estar dentro de los rangos válidos')
        except (TypeError, ValueError):
            errors.append('Latitud y longitud deben ser números válidos')

        try:
            wc_adaptado = bool(wc_adaptado)
            animales_guia = bool(animales_guia)
            asistencia = bool(asistencia)
        except (TypeError, ValueError):
            errors.append(
                'Tipo incorrecto en WC adaptado, animales de guia o asistencia')
        existing_point = PuntoUsuario.objects.filter(
            latitud=latitud, longitud=longitud).first()

        if existing_point and existing_point.user != request.user:
            raise Http404

        if errors:
            return render(request, 'main/nuevo_punto.html', {'errors': errors})

        if existing_point:
            existing_point.nombre = nombre
            existing_point.descripcion = descripcion
            existing_point.amenidad = amenidad
            existing_point.color_accesibilidad = color_accesibilidad
            existing_point.wcAdaptado = wc_adaptado
            existing_point.AnimalesGuia = animales_guia
            existing_point.Asistencia = asistencia
            existing_point.latitud = latitud
            existing_point.longitud = longitud
            existing_point.save()
        else:
            nuevo_punto = PuntoUsuario(
                user=request.user,
                nombre=nombre,
                descripcion=descripcion,
                amenidad=amenidad,
                color_accesibilidad=color_accesibilidad,
                wcAdaptado=wc_adaptado,
                AnimalesGuia=animales_guia,
                Asistencia=asistencia,
                latitud=latitud,
                longitud=longitud,
            )
            nuevo_punto.save()

        return redirect('mapa')


class EliminarPuntoUsuarioView(LoginRequiredMixin, View):
    login_url = 'inicio_sesion'

    def get(self, request):
        punto_id = request.GET.get('id')
        punto = PuntoUsuario.objects.get(pk=punto_id)

        if punto.user == request.user:
            punto.delete()
            return redirect('mapa')
        else:
            raise Http404
