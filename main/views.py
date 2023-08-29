import datetime
from django.shortcuts import render
from django.http import HttpResponse   
from django.shortcuts import render 


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
    return render(
        request,
        'main/mapa.html',
    )