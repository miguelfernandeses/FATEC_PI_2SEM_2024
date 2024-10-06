from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CadastroForm, LoginForm
import logging

def index(request):
    return render(request, "index.html")

logger = logging.getLogger(__name__)

def auth_view(request):
    if request.method == "POST":
        if 'nome' in request.POST:  # Cadastro
            form_cadastro = CadastroForm(request.POST)
            if form_cadastro.is_valid():
                user = form_cadastro.registrar_cliente(request)  # Registra o cliente
                login(request, user)  # Loga o usuário após o cadastro
                return redirect('core:index')  # Redireciona para a página inicial
            else:
                print(form_cadastro.errors)  # Debug: Mostre erros do formulário
                messages.error(request, "Erro ao cadastrar. Verifique os dados.")
        elif 'email' in request.POST:  # Login
            form_login = LoginForm(request.POST)
            if form_login.is_valid():
                email = form_login.cleaned_data.get("email")
                password = form_login.cleaned_data.get("password")
                user = authenticate(username=email, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, "Login bem-sucedido.")
                    return redirect('core:index')
                else:
                    messages.error(request, "Credenciais inválidas.")
    
    return render(request, "auth.html")


def logout_view(request):
    logout(request)
    return redirect('core:index')


@login_required
def meu_perfil(request):
    usuario = request.user
    contexto = {'usuario': usuario}
    return render(request, 'meu_perfil.html', contexto)


