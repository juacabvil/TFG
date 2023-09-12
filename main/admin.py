from django.contrib import admin
from .models import CustomUser, PuntoDeInteres, Aparcamiento

admin.site.register(CustomUser)
admin.site.register(PuntoDeInteres)
admin.site.register(Aparcamiento)