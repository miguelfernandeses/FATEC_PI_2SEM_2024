from django.test import TestCase, Client
from django.shortcuts import resolve_url as r
from django.urls import reverse
from core.models import CadastroModel
from core.forms import CadastroForm
import datetime

'''class CadastroTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.pessoa = {
            'nome': 'João Silva',
            'cpf': '97848729512',
            'email': 'joao.silva@example.com',
            'senha': 'Senha123',
            'data_nasc': '1990-01-01'
        }
        CadastroModel.objects.create(**self.pessoa)
        self.resp = self.client.post(r('core:update'), self.pessoa, follow=True)

    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'cadastro.html')'''

class CadastroviewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.valid_payload = {
            'nome': 'João Silva',
            'email': 'joao.silva@example.com',
            'senha': 'Senha123'
        }
        '''self.invalid_payload = {
            'nome': '9238492',
            'cpf': 'nisancuimao',
            'email': 'joao',
            'senha': '',
            'data_nasc': 'maio'
        }'''
        CadastroModel.objects.create(**self.valid_payload)
        #CadastroModel.objects.create(**self.invalid_payload)
        self.resp = self.client.post(r('core:cadastro'), self.valid_payload)

    '''def test_cadastro_view_success(self):
        response = self.client.post(reverse('core:cadastro'), data=self.valid_payload)
        self.assertEqual(response.status_code, 200)  # Redirecionamento após o cadastro bem-sucedido
        self.assertTrue(CadastroModel.objects.exists())  # Verifica se o usuário foi criado'''

    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'cadastro.html')

    '''def test_cadastro_view_failure(self):
        x = {}
        response = self.client.post(reverse('core:cadastro'), data=self.invalid_payload)
        self.assertEqual(response.status_code, 200)  # Status code 200 indica uma resposta bem-sucedida, mas sem redirecionamento
        self.assertFalse(CadastroModel.objects.filter(**self.invalid_payload).exists())  # Verifica se o usuário não foi criado'''


class CadastroModelTestCase(TestCase):
    def setUp(self):
        self.pessoa = CadastroModel(
            nome='José da Silva',
            email='joao.silva@example.com',
            senha='Senha123')
        self.pessoa.save()

    def test_str(self):
        self.assertEqual(str(self.pessoa), 'José da Silva')

    def test_created(self):
        self.assertTrue(CadastroModel.objects.exists())

    def test_data_saved(self):
        data = CadastroModel.objects.first()
        self.assertEqual(data.nome, 'José da Silva')
        self.assertEqual(data.email, 'joao.silva@example.com')
        self.assertEqual(data.senha, 'Senha123')
        


class cadastroFormTest(TestCase):
    def test_campos_utilizado_cadastro(self):
        form = CadastroForm()
        expected = ['nome', 'email', 'senha']
        self.assertSequenceEqual(expected, list(form.fields))

    def test_form_all_OK(self):
        dados = dict(nome= 'João Silva',
            email= 'joao.silva@example.com',
            senha = 'Senha123.10carac',
        )
        form = CadastroForm(dados)
        errors = form.errors
        self.assertEqual({}, errors)
        self.assertEqual(form.cleaned_data['nome'], 'João Silva')

    def test_form_no_name(self):
        dados = dict(cpf= '97848729512',
            email= 'joao.silva@example.com',
            senha = 'Senha123',
        )
        form = CadastroForm(dados)
        errors = form.errors
        errors_list = errors['nome']
        msg = "Erro ao informar o campo nome."
        self.assertEqual([msg], errors_list)

    def test_form_no_email(self):
        dados = dict(nome= 'João Silva',
            senha = 'Senha123'
        )
        form = CadastroForm(dados)
        errors = form.errors
        errors_list = errors['email']
        msg = "Erro ao informar o campo email."
        self.assertEqual([msg], errors_list)
    
    def test_form_no_senha(self):
        dados = dict(nome= 'João Silva',
            email= 'joao.silva@example.com',
        )
        form = CadastroForm(dados)
        errors = form.errors
        errors_list = errors['senha']
        msg = "Erro ao informar o campo senha."
        self.assertEqual([msg], errors_list)
