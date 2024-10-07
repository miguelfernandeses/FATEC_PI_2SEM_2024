from django import forms
from django.core.exceptions import ValidationError
from .models import CadastroModel
from .services import CadastroClienteService
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
import re

class CadastroForm(forms.ModelForm):
    class Meta:
        model = CadastroModel  # Certifique-se de que esse model está definido corretamente
        fields = ['nome', 'email', 'senha']
        widgets = {
            'senha': forms.PasswordInput(),
        }
        error_messages = {
            'nome': {'required': "Erro ao informar o campo nome."},
            'email': {'required': "Erro ao informar o campo email."},
            'senha': {'required': "Erro ao informar o campo senha."},
        }

    def clean_nome(self):
        nome = self.cleaned_data['nome']
        palavras = [w.capitalize() for w in nome.split()]
        return ' '.join(palavras)

    def clean_email(self):
        email = self.cleaned_data['email']
        if len(re.findall(r"@", email)) != 1 or len(re.findall(r"\.", email)) == 0:
            raise ValidationError('Por favor, insira um email válido.')

        if CadastroModel.objects.filter(email=email).exists():
            raise ValidationError('Este email já está em uso.')

        return email

    def clean_senha(self):
        senha = self.cleaned_data['senha']

        if len(senha) < 8:
            raise ValidationError('Sua senha deve ter pelo menos 8 caracteres.')

        if not any(char.isupper() for char in senha):
            raise ValidationError('Sua senha deve conter pelo menos uma letra maiúscula.')

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha):
            raise ValidationError('Sua senha deve conter pelo menos um caractere especial.')

        return senha

    def registrar_cliente(self, request):
        data = self.cleaned_data
        user = User.objects.create_user(
            username=data['email'],  # Usando email como username
            email=data['email'],
            password=data['senha'],
            first_name=data['nome']  # Se quiser salvar o nome no campo first_name
        )

        # Aqui você pode também salvar no seu model adicional, se necessário
        CadastroModel.objects.create(
            nome=data['nome'],
            email=data['email'],
            senha=data['senha']  # Essa linha pode ser removida se a senha for armazenada no User
        )

        # Loga o usuário imediatamente após o cadastro
        login(request, user)
        messages.success(request, "Cadastro realizado com sucesso!")

class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=254)
    password = forms.CharField(label="Senha", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        user = authenticate(username=email, password=password)
        if user is None:
            raise ValidationError("Email ou senha inválidos.")

        return cleaned_data