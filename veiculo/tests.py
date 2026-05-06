from django.test import TestCase, Client
from datetime import datetime
from django.contrib.auth.models import User

from django.urls import reverse

from veiculo.forms import FormularioVeiculo
from veiculo.models import Veiculo

# Create your tests here.
class TestesModelVeiculo(TestCase):
    # Classe de testes para o modelo Veículo

    instancia = None
    # Primeiro método a ser executado dentro do caso de testes, 
    # onde criamos uma instância do modelo Veículo para ser utilizada nos testes seguintes
    def setUp(self):
        self.instancia = Veiculo(
            marca=1,
            modelo='ABCDE',
            ano=datetime.now().year,
            cor=2,
            combustivel=3
        )

    # Teste para verificar se a propriedade veiculo_novo retorna True para um veículo do ano atual
    def test_veiculo_novo(self):
        self.assertTrue(self.instancia.veiculo_novo) # Verifica se o veículo é considerado novo (ano atual)
        self.instancia.ano = 2025 # Altera o ano para um valor futuro
        self.assertFalse(self.instancia.veiculo_novo) # Verifica se o veículo não é considerado novo (ano diferente do atual)
    
    # Teste para verificar se o método anos_de_uso retorna o valor correto de anos de uso do veículo
    def test_anos_uso(self):
        self.instancia.ano = datetime.now().year - 10
        self.assertEqual(self.instancia.anos_de_uso(), 10)

class TestesViewListarVeiculos(TestCase):
    # Classe de testes para a view ListarVeiculos

    # Primeiro método a ser executado dentro do caso de testes, onde criamos um usuário e um veículo para serem utilizados nos testes seguintes
    def setUp(self):
        self.usuario = User.objects.create(username='teste', password='12345@teste')
        self.client.force_login(self.usuario)
        self.url = reverse('listar-veiculos')
        Veiculo(marca=1, modelo='ABCDE', ano=2, cor=3, combustivel=4).save() # Cria um veículo para ser listado na view

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context.get('veiculos')), 1)

class TestesViewCriarVeiculos(TestCase):
    # Classe de testes para a view CriarVeículos

    def setUp(self):
        self.user = User.objects.create(username='teste', password='12345@teste')
        self.client.force_login(self.user)
        self.url = reverse('criar-veiculo')

    # Teste para verificar se a view redireciona para a página de login quando o usuário não está autenticado
    def test_get_autenticado(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context.get('form'), FormularioVeiculo)

    # Teste para verificar se a view redireciona para a página de login quando o usuário não está autenticado
    def test_get_nao_autenticado(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    # Teste para verificar se a view cria um novo veículo e redireciona para a página de listagem de veículos após o envio do formulário com dados válidos
    def test_post(self):
        dados = {
            'marca': 1,
            'modelo': 'ABCDE',
            'ano': 2,
            'cor': 3,
            'combustivel': 4
        }
        response = self.client.post(self.url, dados)

        # Verifica se após a inserção houve um redirecionamento para a página de listagem de veículos
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('listar-veiculos'))

        self.assertEqual(Veiculo.objects.count(), 1)
        self.assertEqual(Veiculo.objects.first().modelo, 'ABCDE')

class TestesViewEditarVeiculos(TestCase):
    # Classe de testes para a view EditarVeículos

    def setUp(self):
        self.instancia = Veiculo.objects.create(marca=1, modelo='ABCDE', ano=2, cor=3, combustivel=4)
        self.user = User.objects.create(username='teste', password='12345@teste')
        self.client.force_login(self.user)
        self.url = reverse('editar-veiculo', kwargs={'pk': self.instancia.pk})

    # Teste para verificar se a view retorna o formulário preenchido com os dados do veículo a ser editado
    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context.get('object'), Veiculo)
        self.assertIsInstance(response.context.get('form'), FormularioVeiculo)
        self.assertEqual(response.context.get('object').pk, self.instancia.pk)
        self.assertEqual(response.context.get('object').marca, 1)

    def test_post(self):
        dados = {'marca': 5, 'modelo': 'FGHIJ', 'ano': 4, 'cor': 2, 'combustivel': 1}
        response = self.client.post(self.url, dados)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('listar-veiculos'))
        self.assertEqual(Veiculo.objects.count(), 1)
        self.assertEqual(Veiculo.objects.first().marca, 5)
        self.assertEqual(Veiculo.objects.first().pk, self.instancia.pk)

class TestesViewDeletarVeiculos(TestCase):
    # Classe de testes para a view DeletarVeículos

    def setUp(self):
        self.instancia = Veiculo.objects.create(marca=1, modelo='ABCDE', ano=2, cor=3, combustivel=4)
        self.user = User.objects.create(username='teste', password='12345@teste')
        self.client.force_login(self.user)
        self.url = reverse('deletar-veiculo', kwargs={'pk': self.instancia.pk})

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context.get('object'), Veiculo)
        self.assertEqual(response.context.get('object').pk, self.instancia.pk)

    def test_post(self):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('listar-veiculos'))
        self.assertEqual(Veiculo.objects.count(), 0)
    