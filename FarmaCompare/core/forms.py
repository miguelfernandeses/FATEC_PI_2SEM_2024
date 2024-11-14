from django import forms
from django.core.exceptions import ValidationError
from .models import CadastroModel
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
import re

class CadastroForm(forms.ModelForm):
    class Meta:
        model = CadastroModel
        fields = ['email', 'razao_social', 'cnpj', 'telefone', 'endereco', 'senha']
        widgets = {
            'senha': forms.PasswordInput(),
        }
        error_messages = {
            'email': {'required': "Erro ao informar o campo email."},
            'razao_social': {'required': "Erro ao informar o campo razao_social."},
            'cnpj': {'required': "Erro ao informar o campo CNPJ."},
            'telefone': {'required': "Erro ao informar o campo telefone."},
            'endereco': {'required': "Erro ao informar o campo endereco."},
            'senha': {'required': "Erro ao informar o campo senha."},
        }

    def clean_razao_social(self):
        razao_social = self.cleaned_data['razao_social']
        if CadastroModel.objects.filter(razao_social=razao_social).exists():
            self.add_error('razao_social', 'Esta razão social já está em uso.')
        return razao_social


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
    

    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj')
        if CadastroModel.objects.filter(cnpj=cnpj).exists():
            raise ValidationError("Este CNPJ já está em uso.")
    
        if not re.match(r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$', cnpj):
            raise ValidationError("Por favor, insira um CNPJ válido no formato 00.000.000/0000-00.")
        
        return cnpj
    

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        if not re.match(r'^\(\d{2}\) \d{5}-\d{4}$', telefone):
            raise ValidationError('Por favor, insira um telefone válido no formato (00) 00000-0000.')
        return telefone


    def registrar_empresa(self, request):
        data = self.cleaned_data

        if User.objects.filter(username=data['email']).exists():
            raise ValidationError("Este email já está registrado.")

        user = User.objects.create_user(
            username=data['email'], 
            password=data['senha'], 
            first_name=data['razao_social'] 
)
        CadastroModel.objects.create(
            email=data['email'],
            razao_social=data['razao_social'],
            cnpj=data['cnpj'],
            telefone=data['telefone'],
            endereco=data['endereco'],
            senha=data['senha'] 
    )

        login(request, user)
        return user


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
