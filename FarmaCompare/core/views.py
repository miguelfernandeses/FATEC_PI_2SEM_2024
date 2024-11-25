from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CadastroForm, LoginForm
import logging
from .models import Produto, CadastroModel
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

logger = logging.getLogger(__name__)


def index(request):
    try:
        user_id = request.user.id
        usuario = CadastroModel.objects.get(id=user_id)

        plano_atual = usuario.plano

    except CadastroModel.DoesNotExist:
        plano_atual = None 

    return render(request, "index.html", {"plano_atual": plano_atual})

def auth_view(request):
    form_cadastro = CadastroForm()
    form_login = LoginForm()

    if request.method == "POST":
        # Cadastro
        if 'razao_social' in request.POST:
            form_cadastro = CadastroForm(request.POST)
            if form_cadastro.is_valid():
                user = form_cadastro.registrar_empresa(request)
                login(request, user)
                return redirect('core:index')
            else:
                form_cadastro.errors['email'] = form_cadastro.errors.get('email', [])
                form_cadastro.errors['cnpj'] = form_cadastro.errors.get('cnpj', [])

        # Login
        elif 'email' in request.POST:
            form_login = LoginForm(request.POST)
            if form_login.is_valid():
                email = form_login.cleaned_data.get("email")
                password = form_login.cleaned_data.get("password")
                user = authenticate(username=email, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('core:index')
                else:
                    messages.error(request, "Credenciais inválidas. Tente novamente.")

    return render(request, "auth.html", {"form_cadastro": form_cadastro, "form_login": form_login})

#logout
def logout_view(request):
    logout(request)
    logger.info("Usuário deslogado")
    return redirect('core:index')

#meuperfil
@login_required
def meu_perfil(request):
    return render(request, 'meu_perfil.html', {'usuario': request.user})

def get_plano(plano_id):
    planos = {
        1: ("Grátis", "R$ 0,00 / Mês"),
        2: ("Mensal", "R$ 49,90 / Mês"),
        3: ("Anual", "R$ 42,90 / Mês"),
    }
    return planos.get(plano_id, ("Plano inválido", ""))

#Escolher plano
@login_required
def card(request):
    if request.method == "POST":
        plano_id = int(request.POST.get("plano_id"))

        plano_nome, plano_preco = get_plano(plano_id)

        if plano_nome == "Plano inválido":
            messages.error(request, "Plano inválido. Tente novamente.")
            return redirect("core:main")

        return render(request, "card.html", {
            "plano_id": plano_id,
            "plano_nome": plano_nome,
            "plano_preco": plano_preco,
        })
    
    return redirect("core:main")


@login_required
def selecionar_plano(request):
    if request.method == "POST":
        plano = int(request.POST.get("plano_id", 0))
        print(f"Plano selecionado: {plano}")

        if plano not in [1, 2, 3]: 
            messages.error(request, "Plano inválido.")
        else:
            try:
                user_id = request.user.id
                print(f"ID do usuário logado: {user_id}")

                usuario = CadastroModel.objects.get(id=user_id)
                print(f"Usuário encontrado: {usuario}")

                usuario.plano = plano
                
                if plano in [0]:
                    usuario.consultas_restantes = 0 
                elif plano in [2, 3]:
                    usuario.consultas_restantes = 999  
                else:
                    usuario.consultas_restantes = 10 

                usuario.save()
                print(f"Plano do usuário atualizado para: {usuario.plano}, Consultas restantes: {usuario.consultas_restantes}")

                messages.success(request, "Plano atualizado com sucesso!")
                return redirect('core:index')
            except CadastroModel.DoesNotExist:
                print("Erro: Cadastro não encontrado.")
                messages.error(request, "Cadastro não encontrado. Por favor, verifique seus dados.")
                return redirect('core:selecionar_plano')

    return render(request, "card.html")


@login_required
def lista_produtos(request):
    produtos_dsp = Produto.objects.filter(nome_farmacia__iexact="Drogaria São Paulo", price__gt=0)[:20]
    produtos_paguemenos = Produto.objects.filter(nome_farmacia__iexact="Pague Menos",  price__gt=0)[:20]
    produtos_precopopular = Produto.objects.filter(nome_farmacia__iexact="Preço Popular",  price__gt=0)[:20]

    try:
        usuario = CadastroModel.objects.get(id=request.user.id)
        consultas_restantes = usuario.consultas_restantes
    except CadastroModel.DoesNotExist:
        consultas_restantes = 0

    return render(request, 'main.html', {
        'produtos_dsp': produtos_dsp,
        'produtos_paguemenos': produtos_paguemenos,
        'produtos_precopopular': produtos_precopopular,
        'consultas_restantes': consultas_restantes,
    })


@login_required
def search(request):
    query = request.GET.get('q', '')
    page = int(request.GET.get('page', 1))
    limit = 30  # Limitando a 30 produtos
    
    if query:
        produtos = Produto.objects.filter(name__icontains=query)
    
        if produtos.exists():
            paginator = Paginator(produtos, limit)
            produtos_pagina = paginator.get_page(page)
            
            print(f"Produtos na página {page}: {produtos_pagina.object_list}") 
            data = {
                'products': list(produtos_pagina.object_list.values('name', 'nome_farmacia', 'images'))
            }
            return JsonResponse(data)
        else:
            print("Nenhum produto encontrado para o termo de busca.") 
            return JsonResponse({'products': []})

    return JsonResponse({'products': []})


def search_results(request):
    query = request.GET.get('query', '')  # Termo de busca
    offset = int(request.GET.get('offset', 0))  # Offset inicial (padrão 0)
    limit = 50  # Limite de produtos por página
    
    # Filtra os produtos baseados na busca
    produtos = Produto.objects.filter(name__icontains=query)[offset:offset + limit]
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  
        # Retorna os dados em formato JSON
        produtos_data = [
            {
                'id': produto.id,
                'name': produto.name,
                'price': produto.price,
                'images': produto.images,
            }
            for produto in produtos
        ]
        return JsonResponse({'produtos': produtos_data})
    
    # Renderiza o template inicial
    return render(request, 'search_results.html', {'produtos': produtos, 'query': query})


def produto_detalhes(request, name):
    produto = get_object_or_404(Produto, name=name)
    return render(request, 'produto_detalhes.html', {'produto': produto})


@login_required
def produto_detalhe(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)

    outras_farmacias = Produto.objects.filter(
        name__icontains=produto.name
    ).exclude(id=produto.id)[:5] 

    return render(request, 'produto_detalhes.html', {
        'produto': produto,
        'outras_farmacias': outras_farmacias
    })

def busca(request):
    query = request.GET.get('q', '').strip()
    produtos = Produto.objects.all()

    if query:
        produtos = produtos.filter(name__icontains=query) 

    return render(request, 'busca_resultados.html', {'produtos': produtos, 'query': query})

