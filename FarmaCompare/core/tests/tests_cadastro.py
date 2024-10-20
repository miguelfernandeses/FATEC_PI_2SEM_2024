from django.test import TestCase, Client
from django.shortcuts import resolve_url as r
from django.urls import reverse
from core.models import CadastroModel
from core.forms import CadastroForm


class CadastroViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.valid_payload = {
            'nome': 'João Silva',
            'email': 'joao.silva@example.com',
            'senha': 'Senha123'
        }
        self.resp = self.client.post(r('core:cadastro'), self.valid_payload)

    def test_template_used(self):
        """Verifica se o template correto é usado na resposta."""
        self.assertTemplateUsed(self.resp, 'cadastro.html')

    def test_cadastro_view_success(self):
        """Verifica se o cadastro bem-sucedido redireciona corretamente."""
        response = self.client.post(reverse('core:cadastro'), data=self.valid_payload)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(CadastroModel.objects.filter(email=self.valid_payload['email']).exists())


class CadastroModelTestCase(TestCase):

    def setUp(self):
        self.pessoa = CadastroModel(
            nome='José da Silva',
            email='jose.silva@example.com',
            senha='Senha123'
        )
        self.pessoa.save()

    def test_str(self):
        """Verifica a representação em string do modelo."""
        self.assertEqual(str(self.pessoa), 'José da Silva')

    def test_created(self):
        """Verifica se o objeto foi criado no banco de dados."""
        self.assertTrue(CadastroModel.objects.exists())

    def test_data_saved(self):
        """Verifica se os dados foram salvos corretamente."""
        data = CadastroModel.objects.first()
        self.assertEqual(data.nome, 'José da Silva')
        self.assertEqual(data.email, 'jose.silva@example.com')
        self.assertEqual(data.senha, 'Senha123')


class CadastroFormTest(TestCase):

    def test_campos_utilizados_cadastro(self):
        """Verifica se os campos esperados estão presentes no formulário."""
        form = CadastroForm()
        expected = ['nome', 'email', 'senha']
        self.assertSequenceEqual(expected, list(form.fields))

    def test_form_all_ok(self):
        """Verifica se o formulário aceita dados válidos sem erros."""
        dados = {
            'nome': 'João Silva',
            'email': 'joao.silva@example.com',
            'senha': 'Senha123.10carac',
        }
        form = CadastroForm(dados)
        self.assertFalse(form.errors)  # Verifica se não há erros
        self.assertEqual(form.cleaned_data['nome'], 'João Silva')

    def test_form_no_name(self):
        """Verifica se o formulário retorna um erro quando o nome não é informado."""
        dados = {
            'cpf': '97848729512',  # cpf não é um campo no formulário
            'email': 'joao.silva@example.com',
            'senha': 'Senha123',
        }
        form = CadastroForm(dados)
        errors = form.errors
        errors_list = errors['nome']
        msg = "Erro ao informar o campo nome."
        self.assertEqual([msg], errors_list)

    def test_form_no_email(self):
        """Verifica se o formulário retorna um erro quando o email não é informado."""
        dados = {
            'nome': 'João Silva',
            'senha': 'Senha123'
        }
        form = CadastroForm(dados)
        errors = form.errors
        errors_list = errors['email']
        msg = "Erro ao informar o campo email."
        self.assertEqual([msg], errors_list)
    
    def test_form_no_senha(self):
        """Verifica se o formulário retorna um erro quando a senha não é informada."""
        dados = {
            'nome': 'João Silva',
            'email': 'joao.silva@example.com',
        }
        form = CadastroForm(dados)
        errors = form.errors
        errors_list = errors['senha']
        msg = "Erro ao informar o campo senha."
        self.assertEqual([msg], errors_list)
