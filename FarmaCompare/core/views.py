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
from functools import wraps
from django.contrib.auth.decorators import login_required

logger = logging.getLogger(__name__)

def index(request):
    return render(request, "index.html")

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
    # Checa se a requisição é um POST
    if request.method == "POST":
        # Obtém o valor do plano escolhido a partir do formulário
        plano_id = request.POST.get('plano_id')  # O valor do plano escolhido (1, 2, 3)
        
        # Obtém o email do usuário logado que foi passado no formulário
        email = request.POST.get('email')  # O valor do email passado como input oculto
        
        print(f"Plano selecionado: {plano_id}")  # Exibe o valor do plano no console
        print(f"Email recebido: {email}")  # Exibe o email recebido no console
        
        # Verifica se o valor do plano é válido
        if plano_id not in ['1', '2', '3']:  # Verifica se o plano é um dos valores válidos
            messages.error(request, "Plano inválido.")  # Se não for válido, exibe uma mensagem de erro
            print("Erro: Plano inválido.")  # Imprime no console que o plano é inválido
            return redirect('core:index')  # Redireciona para a página inicial

        try:
            # Tenta encontrar o usuário no banco de dados usando o email
            usuario = CadastroModel.objects.get(email=email)  # Procura no banco pelo email
            
            print(f"Usuário encontrado: {usuario}")  # Exibe no console o usuário encontrado
            
            # Se encontrar o usuário, atualiza o plano
            usuario.plano = int(plano_id)  # Converte o plano para inteiro e atribui ao usuário
            usuario.save()  # Salva as alterações no banco de dados
            
            print(f"Plano do usuário atualizado para: {plano_id}")  # Exibe no console o novo plano do usuário
            
            # Aqui você pode usar uma função como 'get_plano' para obter o nome e preço do plano
            plano_nome, plano_preco = get_plano(int(plano_id))
            print(f"Plano selecionado: {plano_nome} - {plano_preco}")  # Exibe no console o nome e preço do plano

            # Exibe uma mensagem de sucesso
            messages.success(request, f"Plano {plano_nome} ({plano_preco}) atualizado com sucesso!")
            
            # Redireciona o usuário para a página inicial
            return redirect('core:index')

        except CadastroModel.DoesNotExist:
            # Caso o usuário com o email informado não seja encontrado, exibe uma mensagem de erro
            messages.error(request, "Cadastro não encontrado.")
            print("Erro: Cadastro não encontrado.")  # Exibe no console o erro
            return redirect('core:index')  # Redireciona para a página inicial

    # Caso a requisição não seja um POST, renderiza o template
    return render(request, 'card.html', {'user': request.user})


def verificar_plano(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        usuario = request.user.cadastro

        if usuario.plano == 1: 
            if usuario.consultas_restantes <= 0:
                return redirect('core:sem_acesso') 
            usuario.consultas_restantes -= 1
            usuario.save()

        elif usuario.plano not in [2, 3]:
            return redirect('core:sem_acesso')

        return func(request, *args, **kwargs)
    return wrapper


@login_required
def lista_produtos(request):
    produtos_dsp = Produto.objects.filter(nome_farmacia__iexact="Drogaria São Paulo", price__gt=0)[:20]
    produtos_paguemenos = Produto.objects.filter(nome_farmacia__iexact="Pague Menos",  price__gt=0)[:20]
    produtos_precopopular = Produto.objects.filter(nome_farmacia__iexact="Preço Popular",  price__gt=0)[:20]

    return render(request, 'main.html', {
        'produtos_dsp': produtos_dsp,
        'produtos_paguemenos': produtos_paguemenos,
        'produtos_precopopular': produtos_precopopular,
    })

#Ultrafarma
#Preço popular
#Pague Menos
#Drogaria Lecer 
#Drogaria São Paulo


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


def produto_detalhes(request, name):
    produto = get_object_or_404(Produto, name=name)
    return render(request, 'produto_detalhes.html', {'produto': produto})


@login_required
@verificar_plano
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

