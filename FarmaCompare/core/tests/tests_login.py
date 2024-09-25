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
            senha='senha123',
            nome='João Silva',
        )
        self.user.save()

    def test_login_view_success(self):
        response = self.client.post(reverse('core:login'), data={
            'email': 'joao.silva@example.com',
            'password': 'Senha.123'
        })
        self.assertEqual(response.status_code, 200) 
        #self.assertTrue(self.client.session.get(self.user))

    '''def test_login_view_failure(self):
        response = self.client.post(reverse('core:login'), data={
            'email': 'invalid@email.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # Status code 200 indica uma resposta bem-sucedida, mas sem redirecionamento
        #self.assertFalse(self.client.session.get('user_id'))  # Verifica se a sessão do usuário não foi iniciada
    '''
class LoginFormTestCase(TestCase):
    def test_campos_utilizados_login(self):
        form = LoginForm()
        expected = ['email', 'password']
        self.assertSequenceEqual(expected, list(form.fields))

class Update_GET_Test(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('core:login'), follow=True)

    def test_status_code(self):
        self.assertEqual(self.resp.status_code , 200)
          
    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'login.html')