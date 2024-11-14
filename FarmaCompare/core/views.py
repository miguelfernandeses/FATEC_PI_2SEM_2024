from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CadastroForm, LoginForm
import logging
from .models import Produto, CadastroModel
from django.core.paginator import Paginator
from django.http import JsonResponse


logger = logging.getLogger(__name__)

def index(request):
    return render(request, "index.html")

def auth_view(request):
    form_cadastro = CadastroForm()
    
    if request.method == "POST":
        if 'razao_social' in request.POST:
            form_cadastro = CadastroForm(request.POST)
            if form_cadastro.is_valid():
                user = form_cadastro.registrar_empresa(request)
                login(request, user)
                return redirect('core:index')
            else:
                form_cadastro.errors['email'] = form_cadastro.errors.get('email', [])
                form_cadastro.errors['cnpj'] = form_cadastro.errors.get('cnpj', [])
        elif 'email' in request.POST:
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

    return render(request, "auth.html", {"form_cadastro": form_cadastro})


def logout_view(request):
    logout(request)
    logger.info("Usuário deslogado")
    return redirect('core:index')

@login_required
def meu_perfil(request):
    return render(request, 'meu_perfil.html', {'usuario': request.user})


@login_required
def escolher_plano(request):
    if request.method == 'POST':
        plano_id = request.POST.get('plano_id')
        if plano_id:
            request.session['plano_selecionado'] = plano_id
        
            return redirect('core:card')
    
    return redirect('core:index')

@login_required
def card(request):
    plano_id = request.session.get('plano_selecionado', None)

    if not plano_id:
        return redirect('core:index')

    if plano_id == '1':
        plano_nome = 'Grátis'
        plano_preco = 'R$ 0,00 / Mês'

    elif plano_id == '2':
        plano_nome = 'Mensal'
        plano_preco = 'R$ 49,90 / Mês'

    elif plano_id == '3':
        plano_nome = 'Anual'
        plano_preco = 'R$ 42,90 / Mês'

    else:
        plano_nome = 'Plano inválido'
        plano_preco = ''

    return render(request, 'card.html', {
        'plano_nome': plano_nome,
        'plano_preco': plano_preco,
    })


def lista_produtos(request):
    produtos = Produto.objects.all()[:20]
    return render(request, 'main.html', {'produtos': produtos})

def search(request):
    query = request.GET.get('q', '')
    page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 20))  
    
    if query:
        produtos = Produto.objects.filter(name__icontains=query)
        
        start = (page - 1) * limit
        end = start + limit
        produtos_pagina = produtos[start:end]
        
        data = {
            'products': list(produtos_pagina.values('name', 'price', 'nome_farmacia'))
        }
        return JsonResponse(data)
    
    return JsonResponse({'products': []})