from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El Email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.password = make_password(password)  
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    family_name = models.CharField(max_length=30)
    second_family_name = models.CharField(max_length=30)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'family_name', 'second_family_name']

    def __str__(self):
        return self.email +' ' +self.password + 'fin'
    
class PuntoDeInteres(models.Model):
    nombre = models.CharField(max_length=100)
    tipo_amenidad = models.CharField(max_length=100, default='Desconocido')
    latitud = models.FloatField()
    longitud = models.FloatField()
    descripcion = models.TextField()
    datos_adicionales = models.JSONField(null=True, blank=True)
    accesibilidad = models.CharField(
    max_length=10, 
    choices=[
        ('yes', 'Yes'),
        ('limited', 'Limited'),
        ('no', 'No'),
        ('designated', 'Designated'),
    ],
    default='no'
)
    


    def __str__(self):
        return self.nombre
    
    CATEGORIAS_AMENIDAD = {
        "Comida": ["restaurant", "cafe", "fast_food", "ice_cream", "food_court"],
        "Entretenimiento": ["cinema", "theatre"],
        "Servicios Financieros": ["bank", "atm"],
        "Bebidas": ["bar", "pub", "drinking_water"],
        "Salud": ["pharmacy", "hospital", "clinic", "dentist", "doctors", "veterinary"],
        "Educación": ["school", "kindergarten", "language_school", "driving_school", "prep_school"],
        "Cultura y Arte": ["arts_centre", "library"],
        "Servicios Públicos": ["police", "post_office", "social_facility", "place_of_worship", "community_centre", "townhall", "shelter", "recycling"],
        "Transporte": ["bicycle_rental", "car_rental", "car_wash"],
        "Otros": ["telephone", "childcare"],
        "Baños": ["toilets"],
        "Fuel": ["fuel"],
    }

    def get_categoria_amenidad(self):
        for categoria, amenidades in self.CATEGORIAS_AMENIDAD.items():
            if self.tipo_amenidad in amenidades:
                return categoria
        return "Desconocida"  

    
    def get_marker_color(self):
        if self.accesibilidad == 'yes':
            return 'green'
        elif self.accesibilidad == 'limited':
            return 'orange'
        elif self.accesibilidad == 'no':
            return 'red'
        elif self.accesibilidad == 'designated':
            return 'blue'
        else:
            return 'gray'  

    def get_marker_icon(self):
        categoria_amenidad = self.get_categoria_amenidad()
        iconos_categoria = {
            "Comida": "bi bi-cup-hot",
            "Entretenimiento": "bi bi-film",
            "Servicios Financieros": "bi bi-bank",
            "Bebidas": "bi bi-cup-straw",
            "Salud": "bi bi-hospital",
            "Educación": "bi bi-book",
            "Cultura y Arte": "bi bi-brush",
            "Servicios Públicos": "bi bi-postcard",
            "Transporte": "bi bi-bicycle",
            "Otros": "bi bi-question",
            "Baños": "bi bi-badge-wc",
            "Fuel": "bi bi-fuel-pump",
            "Desconocida": "bi bi-question",  
        }
        return iconos_categoria.get(categoria_amenidad, "bi bi-question")  
        
    
class Aparcamiento(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    latitud = models.FloatField()
    longitud = models.FloatField()

    def __str__(self):
        return self.nombre
    
    
