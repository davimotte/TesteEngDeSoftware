from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from contas.models import *

class UsuarioUnitTest(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User',
            'tipo': 'familiar'
        }

    def test_usuario_creation(self):
        user = Usuario.objects.create_user(**self.user_data)
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))

    def test_usuario_required_fields(self):
        with self.assertRaises(ValueError):
            Usuario.objects.create_user(email='', password='testpass123')

    def test_superuser_creation(self):
        superuser = Usuario.objects.create_superuser(
            email='admin@example.com',
            password='adminpass123'
        )
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_usuario_string_representation(self):
        user = Usuario.objects.create_user(**self.user_data)
        expected_str = f"{user.email} ({user.get_tipo_display()})"
        self.assertEqual(str(user), expected_str)

    def test_usuario_tipo_choices(self):
        for tipo, display in Usuario.TIPOS:
            with self.subTest(tipo=tipo):
                user = Usuario.objects.create_user(
                    email=f'{tipo}@example.com',
                    password='pass123',
                    tipo=tipo
                )
                self.assertEqual(user.tipo, tipo)
                self.assertEqual(user.get_tipo_display(), display)

class ClinicaUnitTest(TestCase):
    def test_clinica_creation(self):
        clinica = Clinica.objects.create_user(
            email='clinica@example.com',
            password='pass123',
            first_name='Clinica Teste',
            tipo='clinica',
            cnpj='12.345.678/0001-99'
        )
        self.assertEqual(clinica.cnpj, '12.345.678/0001-99')
        self.assertEqual(clinica.tipo, 'clinica')

    def test_clinica_cnpj_uniqueness(self):
        Clinica.objects.create_user(
            email='clinica1@example.com',
            password='pass123',
            cnpj='12.345.678/0001-99'
        )
        with self.assertRaises(IntegrityError):
            Clinica.objects.create_user(
                email='clinica2@example.com',
                password='pass123',
                cnpj='12.345.678/0001-99'
            )

class TerapeutaUnitTest(TestCase):
    def test_terapeuta_creation(self):
        terapeuta = Terapeuta.objects.create_user(
            email='terapeuta@example.com',
            password='pass123',
            first_name='Dr. Silva',
            tipo='terapeuta',
            crp='12345/SP'
        )
        self.assertEqual(terapeuta.crp, '12345/SP')
        self.assertEqual(terapeuta.tipo, 'terapeuta')

    def test_terapeuta_crp_uniqueness(self):
        Terapeuta.objects.create_user(
            email='terapeuta1@example.com',
            password='pass123',
            crp='12345/SP'
        )
        with self.assertRaises(IntegrityError):
            Terapeuta.objects.create_user(
                email='terapeuta2@example.com',
                password='pass123',
                crp='12345/SP'
            )

class FamiliarUnitTest(TestCase):
    def test_familiar_creation(self):
        familiar = Familiar.objects.create_user(
            email='familiar@example.com',
            password='pass123',
            first_name='Maria',
            tipo='familiar',
            parentesco='Mãe'
        )
        self.assertEqual(familiar.parentesco, 'Mãe')
        self.assertEqual(familiar.tipo, 'familiar')

class PacienteUnitTest(TestCase):
    
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            email='usuario@example.com',
            password='pass123',
            first_name='João'
        )
        self.clinica = Clinica.objects.create_user(
            email='clinica@example.com',
            password='pass123',
            first_name='Clinica Teste',
            tipo='clinica'
        )

    def test_paciente_creation(self):
        paciente = Paciente.objects.create(
            usuario=self.usuario,
            data_nascimento='2010-01-01',
            neurodivergencia='TEA',
            clinica=self.clinica
        )
        self.assertEqual(paciente.neurodivergencia, 'TEA')
        self.assertEqual(paciente.clinica, self.clinica)

    def test_paciente_methods(self):
        paciente = Paciente.objects.create(
            usuario=self.usuario,
            data_nascimento='2010-01-01',
            neurodivergencia='TDAH',
            clinica=self.clinica
        )
        
        # Testa método get_familiares_vinculados (deve retornar QuerySet vazia inicialmente)
        familiares = paciente.get_familiares_vinculados()
        self.assertEqual(familiares.count(), 0)

class EnderecoUnitTest(TestCase):
    
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            email='user@example.com',
            password='pass123',
            first_name='Test'
        )

    def test_endereco_creation(self):
        endereco = Endereco.objects.create(
            usuario=self.usuario,
            rua='Rua Teste',
            numero='123',
            bairro='Centro',
            cidade='São Paulo',
            estado='SP',
            cep='01234-567'
        )
        self.assertEqual(endereco.cidade, 'São Paulo')
        self.assertEqual(endereco.usuario, self.usuario)

class ModelMethodsUnitTest(TestCase):
    
    def test_familiar_registrar_comentario_method(self):
        familiar = Familiar.objects.create_user(
            email='familiar@example.com',
            password='pass123',
            first_name='Maria',
            tipo='familiar'
        )
        
        clinica = Clinica.objects.create_user(
            email='clinica@example.com',
            password='pass123',
            first_name='Clinica',
            tipo='clinica'
        )
        
        usuario_paciente = Usuario.objects.create_user(
            email='paciente@example.com',
            password='pass123',
            first_name='João'
        )
        
        paciente = Paciente.objects.create(
            usuario=usuario_paciente,
            data_nascimento='2010-01-01',
            neurodivergencia='TEA',
            clinica=clinica
        )
        self.assertIsNotNone(familiar)
        self.assertIsNotNone(paciente)