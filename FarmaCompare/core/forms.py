from django import forms
from django.core.exceptions import ValidationError
from .models import CadastroModel
import re

class CadastroForm(forms.ModelForm):
    class Meta:
        model = CadastroModel
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
        return email

    def clean_senha(self):
        senha = self.cleaned_data['senha']

        if len(senha) < 8:  # Corrigido para 8 caracteres
            raise ValidationError('Sua senha deve ter pelo menos 8 caracteres.')

        if not any(char.isupper() for char in senha):
            raise ValidationError('Sua senha deve conter pelo menos uma letra maiúscula.')

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha):
            raise ValidationError('Sua senha deve conter pelo menos um caractere especial.')

        return senha


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=254)
    password = forms.CharField(label="Senha", widget=forms.PasswordInput)
