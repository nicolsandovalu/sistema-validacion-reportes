from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from core.models import Profesor, Registro

class SistemaValidacionTests(TestCase):
    def setUp(self):
        # 1. Configurar cliente y grupos
        self.client = Client()
        self.grupo_admin = Group.objects.create(name='admin')
        self.grupo_viewer = Group.objects.create(name='viewer')
        
        # 2. Crear usuarios de prueba
        self.user_admin = User.objects.create_user(username='admin_test', password='password123')
        self.user_admin.groups.add(self.grupo_admin)
        
        self.user_viewer = User.objects.create_user(username='viewer_test', password='password123')
        self.user_viewer.groups.add(self.grupo_viewer)

        # 3. Crear datos base
        self.profesor = Profesor.objects.create(
            nombre="Profesor Prueba", 
            correo="prueba@institucion.cl"
        )
        self.registro = Registro.objects.create(
            profesor=self.profesor,
            programa="Programa Test",
            cantidad=10,
            estado="Activo"
        )

    def test_generacion_automatica_token(self):
        """Prueba que al crear un profesor se le asigne un token único automáticamente"""
        self.assertIsNotNone(self.profesor.token)
        self.assertEqual(len(self.profesor.token), 6) # secrets.token_hex(3) genera 6 caracteres

    def test_borrado_logico(self):
        """Prueba que el soft_delete oculte el registro sin destruirlo"""
        self.assertFalse(self.registro.eliminado)
        self.assertIsNone(self.registro.fecha_eliminacion)
        
        # Ejecutar borrado lógico
        self.registro.soft_delete()
        
        self.assertTrue(self.registro.eliminado)
        self.assertIsNotNone(self.registro.fecha_eliminacion)
        # Verificar que sigue existiendo en la base de datos (no se borró físicamente)
        self.assertEqual(Registro.objects.count(), 1)

    def test_seguridad_vistas_sin_login(self):
        """Prueba que un usuario no autenticado sea expulsado al login"""
        response = self.client.get(reverse('gestion_reportes'))
        self.assertRedirects(response, '/login/?next=/gestion-reportes/')

    def test_seguridad_vistas_con_rol_incorrecto(self):
        """Prueba que un usuario sin rol de admin sea rechazado por el decorador"""
        self.client.login(username='viewer_test', password='password123')
        # gestion_reportes requiere rol 'admin' o 'normal'
        response = self.client.get(reverse('gestion_reportes'))
        self.assertRedirects(response, reverse('login'))

    def test_seguridad_vistas_con_rol_correcto(self):
        """Prueba que el administrador sí pueda entrar al dashboard"""
        self.client.login(username='admin_test', password='password123')
        response = self.client.get(reverse('gestion_reportes'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gestion_reportes.html')