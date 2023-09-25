from django.contrib import admin
from .models import CustomUser, PuntoDeInteres, Aparcamiento, PuntoUsuario, Opinion

admin.site.register(CustomUser)
admin.site.register(PuntoDeInteres)
admin.site.register(Aparcamiento)
admin.site.register(PuntoUsuario)
admin.site.register(Opinion)