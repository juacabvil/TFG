from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import PuntoDeInteres, PuntoUsuario, Aparcamiento, Opinion
from django.test import Client
from django.core.exceptions import ObjectDoesNotExist

from selenium import webdriver
from django.test import LiveServerTestCase



User = get_user_model()

class ProcesarOpinionTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpassword',
            first_name='Test',
            family_name='User',
            second_family_name='Custom'
        )

        self.punto_interes = PuntoDeInteres.objects.create(
            nombre='Ejemplo Punto de Interés',
            latitud=0.0,  
            longitud=0.0, 
            descripcion='Descripción de ejemplo'
        )
        self.punto_usuario = PuntoUsuario.objects.create(
            nombre='Ejemplo Punto Usuario',
            latitud=0.0,  
            longitud=0.0,  
            descripcion='Descripción de ejemplo',
            user=self.user
        )
        self.aparcamiento = Aparcamiento.objects.create(
            nombre='Ejemplo Aparcamiento',
            latitud=0.0,  
            longitud=0.0,  
            descripcion='Descripción de ejemplo'
        )

    def test_procesar_opinion_logeado(self):
        self.client.login(email='test@example.com', password='testpassword')
        response = self.client.post(reverse('procesar_opinion'), {
            'texto_opinion': 'Esta es una opinión de prueba',
            'punto_id': self.punto_interes.id,
            'punto_tipo': 'punto_de_interes'
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Opinion.objects.count(), 1)
        opinion = Opinion.objects.first()
        self.assertEqual(opinion.usuario, self.user)
        self.assertEqual(opinion.texto, 'Esta es una opinión de prueba')
        self.assertEqual(opinion.punto_interes, self.punto_interes)

    def test_procesar_opinion_no_logeado(self):
        response = self.client.post(reverse('procesar_opinion'), {
            'texto_opinion': 'Esta es una opinión de prueba',
            'punto_id': self.punto_usuario.id,
            'punto_tipo': 'punto_usuario'
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Opinion.objects.count(), 0)
        self.assertEqual(response.json(), {'status': 'error', 'message': 'Debes iniciar sesión para enviar una opinión'})

    def test_procesar_opinion_sin_texto(self):
        self.client.login(email='test@example.com', password='testpassword')
        response = self.client.post(reverse('procesar_opinion'), {
            'texto_opinion': '',
            'punto_id': self.aparcamiento.id,
            'punto_tipo': 'aparcamiento'
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Opinion.objects.count(), 0)
        self.assertEqual(response.json(), {'status': 'error', 'message': 'El texto de la opinión no puede estar en blanco'})

    def test_procesar_opinion_punto_invalido(self):
        self.client.login(email='test@example.com', password='testpassword')
        response = self.client.post(reverse('procesar_opinion'), {
            'texto_opinion': 'Otra opinión de prueba',
            'punto_id': self.punto_interes.id,
            'punto_tipo': 'punto_invalido'
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Opinion.objects.count(), 0)
        self.assertEqual(response.json(), {'status': 'error', 'message': 'Tipo de punto no válido'})
        
    def test_procesar_opinion_existente(self):
        self.client.login(email='test@example.com', password='testpassword')

        existing_opinion = Opinion.objects.create(
            usuario=self.user,
            texto='Opinión existente',
            punto_interes=self.punto_interes
        )

        response = self.client.post(reverse('procesar_opinion'), {
            'texto_opinion': 'Nueva opinión para punto de interés',
            'punto_id': self.punto_interes.id,
            'punto_tipo': 'punto_de_interes'
        })

        self.assertEqual(response.status_code, 200)
        existing_opinion.refresh_from_db()
        self.assertEqual(existing_opinion.texto, 'Nueva opinión para punto de interés')

    def test_procesar_opinion_existente_punto_usuario(self):
        self.client.login(email='test@example.com', password='testpassword')
        existing_opinion = Opinion.objects.create(
            usuario=self.user,
            texto='Opinión existente para punto usuario',
            punto_usuario=self.punto_usuario
        )

        response = self.client.post(reverse('procesar_opinion'), {
            'texto_opinion': 'Nueva opinión para punto usuario',
            'punto_id': self.punto_usuario.id,
            'punto_tipo': 'punto_usuario'
        })

        self.assertEqual(response.status_code, 200)

        # Verificar que la opinión existente se haya actualizado
        existing_opinion.refresh_from_db()
        self.assertEqual(existing_opinion.texto, 'Nueva opinión para punto usuario')

    def test_procesar_opinion_existente_aparcamiento(self):
        self.client.login(email='test@example.com', password='testpassword')

        # Crear una opinión existente para el aparcamiento
        existing_opinion = Opinion.objects.create(
            usuario=self.user,
            texto='Opinión existente para aparcamiento',
            aparcamiento=self.aparcamiento
        )

        response = self.client.post(reverse('procesar_opinion'), {
            'texto_opinion': 'Nueva opinión para aparcamiento',
            'punto_id': self.aparcamiento.id,
            'punto_tipo': 'aparcamiento'
        })

        self.assertEqual(response.status_code, 200)

        # Verificar que la opinión existente se haya actualizado
        existing_opinion.refresh_from_db()
        self.assertEqual(existing_opinion.texto, 'Nueva opinión para aparcamiento')
        

class RegistroViewTestCase(TestCase):
    
    def test_get_request(self):
        response = self.client.get(reverse('registro')) 
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/registro.html')

    def test_post_valid(self):
        response = self.client.post(reverse('registro'), {
            'email': 'test@example.com',
            'password1': '1q2w3e4r!',
            'password2': '1q2w3e4r!',
            'first_name': 'Test',
            'family_name': 'User',
            'second_family_name': 'Custom',
        })
        self.assertRedirects(response, reverse('mapa'), status_code=302)
        
        self.assertTrue(User.objects.filter(email='test@example.com').exists())
    

    def test_formatos_email(self):
        invalid_emails = ['invalid_email', 'user@', 'user@domain', 'user@.com']
        for email in invalid_emails:
            response = self.client.post(reverse('registro'), {
                'email': email,
                'password1': 'testpassword',
                'password2': 'testpassword',
                'first_name': 'Test',
                'family_name': 'User',
                'second_family_name': 'Custom',
                
            })
            self.assertEqual(response.status_code, 200) 
            self.assertFalse(User.objects.filter(email=email).exists())

    def test_passwords_debil(self):
        weak_passwords = ['12345678', 'abcdefg', 'Test1234']
        for password in weak_passwords:
            response = self.client.post(reverse('registro'), {
                'email': 'valid_email@example.com',
                'password1': password,
                'password2': password,
                'first_name': 'Test',
                'family_name': 'User',
                'second_family_name': 'Custom',
            })
            self.assertEqual(response.status_code, 200) 
            self.assertFalse(User.objects.filter(email='valid_email@example.com').exists())

class InicioSesionViewTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='testpassword'
        )
        self.login_url = reverse('inicio_sesion')

    def test_get_login_page(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/inicio_sesion.html')

    def test_login_valid_user(self):
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 302)  
        self.assertRedirects(response, reverse('mapa'))

    def test_login_invalid_user(self):
        data = {
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 200)
        
        messages = response.context['messages']
        error_messages = [str(message) for message in messages]
        self.assertIn('Usuario o contraseña incorrectos', error_messages)


    def test_login_with_next(self):
        next_url = reverse('mapa')  
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(f'{self.login_url}?next={next_url}', data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, next_url)


class NuevoPuntoViewTestCaseGet(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='testpassword'
        )

    def test_get_punto_owner(self):
        punto = PuntoUsuario.objects.create(
            user=self.user,
            nombre='Mi Punto',
            latitud=1.0,
            longitud=2.0
        )
        get_params = {
            'latitud': punto.latitud,
            'longitud': punto.longitud,
        }
        self.client.force_login(self.user)
        response = self.client.get(reverse('nuevo_punto'), get_params)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/nuevo_punto.html')
        self.assertEqual(response.context['punto'], punto)

    def test_get_punto_no_owner(self):
        otro_usuario = get_user_model().objects.create_user(
            email='otheruser@example.com',
            password='otherpassword'
        )
        punto = PuntoUsuario.objects.create(
            user=otro_usuario,
            nombre='Punto de otro usuario',
            latitud=3.0,
            longitud=4.0
        )

        get_params = {
            'latitud': punto.latitud,
            'longitud': punto.longitud,
        }
        self.client.force_login(self.user)
        response = self.client.get(reverse('nuevo_punto'), get_params)

        self.assertEqual(response.status_code, 404)

    def test_get_punto_nuevo(self):
        
        get_params = {
            'latitud': 5.0,
            'longitud': 6.0,
        }
        self.client.force_login(self.user)
        response = self.client.get(reverse('nuevo_punto'), get_params)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/nuevo_punto.html')
        self.assertIsNone(response.context.get('punto'))
    
    
class NuevoPuntoViewTestCasePost(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='testpassword'
        )

    def test_post_point(self):
        data = {
            'nombre': 'Nuevo Punto de Prueba',
            'descripcion': 'Descripción de prueba',
            'amenidad': 'Comida',
            'color_accesibilidad': 'red',
            'wcAdaptado': 'on',
            'AnimalesGuia': 'on',
            'Asistencia': 'on',
            'latitud': 1.0, 
            'longitud': 2.0,
        }

        self.client.force_login(self.user)
        response = self.client.post(reverse('nuevo_punto') + f'?latitud={data["latitud"]}&longitud={data["longitud"]}', data, follow=True)
        
        self.assertEqual(response.status_code, 200)
        punto = PuntoUsuario.objects.get(latitud=1.0,longitud=2.0 )
        self.assertEqual(punto.nombre,'Nuevo Punto de Prueba')
        

    def test_post_update_point(self):
        
        punto = PuntoUsuario.objects.create(
            user=self.user,
            nombre='Mi Punto Existente',
            latitud=1.0,
            longitud=2.0
        )
        data = {
            'nombre': 'Nuevo Nombre para Punto Existente',
            'descripcion': 'Descripción actualizada',
            'amenidad': 'Comida',
            'color_accesibilidad': 'red',
            'wcAdaptado': 'on',
            'AnimalesGuia': 'on',
            'Asistencia': 'on',
            'latitud': 2.0, 
            'longitud': 2.0,
        }

        self.client.force_login(self.user)
        response = self.client.post(reverse('nuevo_punto') + f'?latitud={data["latitud"]}&longitud={data["longitud"]}', data, follow=True)

        self.assertEqual(response.status_code, 200)
        puntobd = PuntoUsuario.objects.get(latitud=2.0,longitud=2.0)
        self.assertEqual(puntobd.nombre, 'Nuevo Nombre para Punto Existente')
    
    def test_post_point_no_logged(self):
        data = {
            'nombre': 'Nuevo Punto de Prueba',
            'descripcion': 'Descripción de prueba',
            'amenidad': 'Comida',
            'color_accesibilidad': 'red',
            'wcAdaptado': 'on',
            'AnimalesGuia': 'on',
            'Asistencia': 'on',
            'latitud': 3.0, 
            'longitud': 2.0,
        }
        self.client.logout()
        response = self.client.post(reverse('nuevo_punto') + f'?latitud={data["latitud"]}&longitud={data["longitud"]}', data, follow=True)

        self.assertEqual(response.status_code, 200)  

        try:
            puntobd = PuntoUsuario.objects.get(latitud=3.0, longitud=2.0)
        except ObjectDoesNotExist:
            puntobd = None

        self.assertIsNone(puntobd, "Se esperaba que el punto no existiera")
        
    def test_post_errors(self):
        
        
        post_params = {
            'nombre': '',  
            'descripcion': 'Descripción no válida'+'a'*2000,
            'amenidad': 'algo aleatorio no valido',
            'color_accesibilidad': 'algo aleatorio no valido',
            'wcAdaptado': 'algo aleatorio no romperá el check',
            'AnimalesGuia': 'AnimalesGuia',
            'Asistencia': 'Asistencia',
            'latitud': 10000.0,
            'longitud': 0.0,
        }
        self.client.force_login(self.user)
        response = self.client.post(reverse('nuevo_punto') + f'?latitud={post_params["latitud"]}&longitud={post_params["longitud"]}', post_params, follow=True)

        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/nuevo_punto.html')

        
        errors = response.context.get('errors', [])
        self.assertTrue(errors)
        self.assertIn('El nombre es obligatorio', errors)
        self.assertIn('La descripción no puede tener más de 2000 caracteres', errors)
        self.assertIn('Categoría de amenidad no válida', errors)
        self.assertIn('Nivel de accesibilidad no válido', errors)
        self.assertIn('Latitud y longitud deben estar dentro de los rangos válidos', errors)

    def test_post_error_long_name(self):
        
        post_params = {
            'nombre': 'a' * 101,  
            'descripcion': 'Descripción válida',
            'amenidad': PuntoUsuario.CATEGORIAS_AMENIDAD_CHOICES[0][0],
            'color_accesibilidad': PuntoUsuario.COLOR_CHOICES[0][0],
            'wcAdaptado': 'wcAdaptado',
            'AnimalesGuia': 'AnimalesGuia',
            'Asistencia': 'Asistencia',
            'latitud': 0.0,
            'longitud': 0.0,
        }
        self.client.force_login(self.user)
        response = self.client.post(reverse('nuevo_punto'), post_params)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/nuevo_punto.html')

        errors = response.context.get('errors', [])
        self.assertTrue(errors)
        self.assertIn('El nombre no puede tener más de 100 caracteres', errors)
    
    def test_post_update_owner(self):
        punto = PuntoUsuario.objects.create(
            user=self.user,
            nombre='Mi Punto',
            latitud=1.0,
            longitud=2.0
        )

        post_params = {
            'nombre': 'Nuevo Nombre para Punto Existente',
            'descripcion': 'Descripción actualizada',
            'amenidad': 'Comida',
            'color_accesibilidad': 'red',
            'wcAdaptado': 'on',
            'AnimalesGuia': 'on',
            'Asistencia': 'on',
            'latitud': 1.0, 
            'longitud': 2.0,
        }

        self.client.force_login(self.user)
        response = self.client.post(reverse('nuevo_punto') + f'?latitud={post_params["latitud"]}&longitud={post_params["longitud"]}', post_params, follow=True)

        self.assertEqual(response.status_code, 200)
        puntobd = PuntoUsuario.objects.get(latitud=1.0, longitud=2.0)
        self.assertEqual(puntobd.nombre, 'Nuevo Nombre para Punto Existente')

    def test_post_update_no_owner(self):
        otro_usuario = get_user_model().objects.create_user(
            email='otheruser@example.com',
            password='otherpassword'
        )
        punto = PuntoUsuario.objects.create(
            user=otro_usuario,
            nombre='Punto de otro usuario',
            latitud=3.0,
            longitud=4.0
        )

        post_params = {
            'nombre': 'Nuevo Nombre para Punto Existente',
            'descripcion': 'Descripción actualizada',
            'amenidad': 'Comida',
            'color_accesibilidad': 'red',
            'wcAdaptado': 'on',
            'AnimalesGuia': 'on',
            'Asistencia': 'on',
            'latitud': 3.0, 
            'longitud': 4.0,
        }

        self.client.force_login(self.user)
        response = self.client.post(reverse('nuevo_punto') + f'?latitud={post_params["latitud"]}&longitud={post_params["longitud"]}', post_params, follow=True)

        self.assertEqual(response.status_code, 404)

    def test_post_update_errors(self):
        punto = PuntoUsuario.objects.create(
            user=self.user,
            nombre='Mi Punto',
            latitud=1.0,
            longitud=2.0
        )

        post_params = {
            'nombre': 'a' * 101,  
            'descripcion': 'Descripción válida',
            'amenidad': 'Comida',
            'color_accesibilidad': 'red',
            'wcAdaptado': 'wcAdaptado',
            'AnimalesGuia': 'AnimalesGuia',
            'Asistencia': 'Asistencia',
            'latitud': 1.0, 
            'longitud': 2.0,
        }

        self.client.force_login(self.user)
        response = self.client.post(reverse('nuevo_punto') + f'?latitud={post_params["latitud"]}&longitud={post_params["longitud"]}', post_params, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/nuevo_punto.html')
        errors = response.context.get('errors', [])
        self.assertTrue(errors)
        self.assertIn('El nombre no puede tener más de 100 caracteres', errors)
        
      
class EliminarPuntoUsuarioViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='testpassword'
        )
        self.user2 = get_user_model().objects.create_user(
            email='testuser2@example.com',
            password='testpassword2'
        )
        self.punto = PuntoUsuario.objects.create(
            user=self.user,
            nombre='Mi Punto',
            latitud=1.0,
            longitud=2.0
        )

    def test_delete_point_owner(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('eliminar_punto') + f'?id={self.punto.id}')

        self.assertEqual(response.status_code, 302)
        self.assertFalse(PuntoUsuario.objects.filter(pk=self.punto.id).exists())

    def test_delete_point_no_owner(self):
        self.client.force_login(self.user2)
        response = self.client.get(reverse('eliminar_punto') + f'?id={self.punto.id}')

        self.assertEqual(response.status_code, 404)  

    def test_delete_point_not_logged(self):
        self.client.logout()
        response = self.client.get(reverse('eliminar_punto') + f'?id={self.punto.id}')

        self.assertEqual(response.status_code, 302)  
        self.assertTrue(PuntoUsuario.objects.filter(pk=self.punto.id).exists())
        

class MapaViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser', password='testpassword')
        self.punto_usuario = PuntoUsuario.objects.create(
            user=self.user,
            nombre='Mi Punto de Usuario',
            latitud=1.0,
            longitud=2.0,
        )
        self.punto_interes = PuntoDeInteres.objects.create(
            nombre='Punto de Interés',
            latitud=3.0,
            longitud=4.0,
        )
        self.aparcamiento = Aparcamiento.objects.create(
            nombre='Aparcamiento',
            latitud=5.0,
            longitud=6.0,
        )

    def test_mapa_view_logged_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('mapa'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mi Punto de Usuario')
        self.assertContains(response, 'Punto de Interés')
        self.assertContains(response, 'Aparcamiento')

    def test_mapa_view_anonymous_user(self):
       
        response = self.client.get(reverse('mapa'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mi Punto de Usuario')
        self.assertContains(response, 'Punto de Interés')
        self.assertContains(response, 'Aparcamiento')
       
     

class SeleniumTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome()
        
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_home_page_loads(self):
        self.driver.get(self.live_server_url)
        self.assertIn('Sevidis', self.driver.title)
    
    def test_mapa_page_loads(self):
        self.driver.get(self.live_server_url + '/mapa')
        self.assertIn('Sevidis', self.driver.title)
            
        


    
        
