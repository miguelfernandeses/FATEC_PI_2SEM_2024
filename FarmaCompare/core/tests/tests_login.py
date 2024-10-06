from django.test import TestCase, Client
from django.urls import reverse
from core.models import CadastroModel
from core.forms import LoginForm
from django.shortcuts import resolve_url as r

class LoginViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = CadastroModel.objects.create(
            email='joao.silva@example.com',
            senha='Senha.123',  # Corrigido para a senha válida usada no login
            nome='João Silva',
        )

    def test_login_view_success(self):
        """Verifica se o login bem-sucedido retorna o status correto."""
        response = self.client.post(reverse('core:login'), data={
            'email': 'joao.silva@example.com',
            'password': 'Senha.123'  # A senha deve ser a mesma usada ao criar o usuário
        })
        self.assertEqual(response.status_code, 302)  # Redirecionamento após login bem-sucedido

    def test_login_view_failure(self):
        """Verifica se o login falha com credenciais inválidas."""
        response = self.client.post(reverse('core:login'), data={
            'email': 'invalid@email.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # Status 200 indica que a página de login foi retornada
        # Verifica se a sessão do usuário não foi iniciada
        self.assertNotIn('_auth_user_id', self.client.session)  # Verifica se o usuário não está autenticado


class LoginFormTestCase(TestCase):

    def test_campos_utilizados_login(self):
        """Verifica se os campos esperados estão presentes no formulário de login."""
        form = LoginForm()
        expected = ['email', 'password']
        self.assertSequenceEqual(expected, list(form.fields))


class UpdateGETTest(TestCase):

    def setUp(self):
        self.client = Client()  # Adiciona Client no setUp
        self.resp = self.client.get(r('core:login'), follow=True)

    def test_status_code(self):
        """Verifica se a página de login retorna o status correto."""
        self.assertEqual(self.resp.status_code, 200)

    def test_template_used(self):
        """Verifica se o template correto é usado na resposta."""
        self.assertTemplateUsed(self.resp, 'login.html')
