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
from django.http import HttpResponse
from django.db.models import Q 
from django.contrib import messages
from .forms import EditarCadastroForm


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
        if 'razao_social' in request.POST:  # Indica que o formulário de cadastro foi enviado
            form_cadastro = CadastroForm(request.POST)
            if form_cadastro.is_valid():
                user = form_cadastro.registrar_empresa(request)
                login(request, user)
                return redirect('core:index')
            else:
                # Define um contexto específico para os erros de cadastro
                return render(request, "auth.html", {
                    "form_cadastro": form_cadastro,
                    "form_login": LoginForm(),  # Reseta o formulário de login
                })

        # Login
        elif 'email' in request.POST:  # Indica que o formulário de login foi enviado
            form_login = LoginForm(request.POST)
            if form_login.is_valid():
                email = form_login.cleaned_data.get("email")
                password = form_login.cleaned_data.get("password")
                user = authenticate(request, username=email, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('core:index')
                else:
                    messages.error(request, "Credenciais inválidas. Tente novamente.")
            # Define um contexto específico para os erros de login
            return render(request, "auth.html", {
                "form_cadastro": CadastroForm(),  # Reseta o formulário de cadastro
                "form_login": form_login,
            })

    # Carregar a página com os dois formulários sem erros por padrão
    return render(request, "auth.html", {
        "form_cadastro": form_cadastro,
        "form_login": form_login,
    })

#
@login_required
def logout_view(request):
    logout(request)
    logger.info("Usuário deslogado")
    return redirect('core:index')

@login_required
def minha_conta(request):
    if request.user.is_authenticated:
        try:
            cadastro = CadastroModel.objects.get(id=request.user.id)
        except CadastroModel.DoesNotExist:
            cadastro = None
    else:
        cadastro = None
    
    return render(request, 'minha_conta.html', {'cadastro': cadastro})

@login_required
def editar_conta(request):
    cadastro = CadastroModel.objects.get(id=request.user.id)
    
    if request.method == 'POST':
        form = EditarCadastroForm(request.POST, instance=cadastro)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Informações atualizadas com sucesso!")
            return redirect('minha-conta')
        else:
            logging.debug(f"Erros no formulário: {form.errors}")
    else:
        form = EditarCadastroForm(instance=cadastro)

    return render(request, 'editar-conta.html', {'form': form})

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
                
                if plano in [1]:
                    usuario.consultas_restantes = 10 
                elif plano in [2, 3]:
                    usuario.consultas_restantes = 999  
                else:
                    usuario.consultas_restantes = 0 

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
    produtos_dograriapacheco = Produto.objects.filter(nome_farmacia__iexact="Drogarias Pacheco",  price__gt=0)[:20]
    produtos_extrafarma = Produto.objects.filter(nome_farmacia__iexact="Extrafarma",  price__gt=0)[:20]

    try:
        usuario = CadastroModel.objects.get(id=request.user.id)
        consultas_restantes = usuario.consultas_restantes
    except CadastroModel.DoesNotExist:
        consultas_restantes = 0

    return render(request, 'main.html', {
        'produtos_dsp': produtos_dsp,
        'produtos_drogariapacheco': produtos_dograriapacheco,
        'produtos_extrafarma': produtos_extrafarma,
        'consultas_restantes': consultas_restantes,
    })


@login_required
def search(request):
    query = request.GET.get('q', '')
    page = int(request.GET.get('page', 1))
    limit = 30  # Limitando a 30 produtos

    if query:
        # Adiciona a validação para não trazer produtos com price igual a 0
        produtos = Produto.objects.filter(
            Q(name__icontains=query) & ~Q(price=0)
        )
        
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


@login_required
def produto_detalhes(request, name, nome_farmacia):
    produtos = Produto.objects.filter(name=name, nome_farmacia=nome_farmacia)
    if produtos.count() == 1:
        produto = produtos.first()
        mensagem = None
    elif produtos.count() > 1:
        produto = produtos.first()
        mensagem = "Existem múltiplos produtos com esse nome. Exibindo o primeiro."
    else:
        return HttpResponse("Produto não encontrado.", status=404)

    outras_farmacias = Produto.objects.filter(ean=produto.ean).exclude(id=produto.id)[:5]

    return render(request, 'produto_detalhes.html', {
        'produto': produto,
        'outras_farmacias': outras_farmacias,
        'mensagem': mensagem
    })


@login_required
def produtos_detalhe(request, ean, nome_farmacia):
    try:
        produto = Produto.objects.get(ean=ean, nome_farmacia=nome_farmacia)
    except Produto.DoesNotExist:
        return HttpResponse("Produto não encontrado.", status=404)

    outras_farmacias = Produto.objects.filter(ean=produto.ean).exclude(nome_farmacia=nome_farmacia)

    return render(request, 'produto_detalhes.html', {
        'produto': produto,
        'outras_farmacias': outras_farmacias,
    })


@login_required
def busca(request):
    query = request.GET.get('q', '').strip()
    page = int(request.GET.get('page', 1)) 

    produtos = Produto.objects.all()

    if query:
        produtos = produtos.filter(name__icontains=query) 

    produtos_validos = []
    for produto in produtos:
        try:
            produto_url = f"/produto/{produto.name}/{produto.nome_farmacia}/"
            produtos_validos.append(produto)
        except Exception as e:
            continue

    paginator = Paginator(produtos_validos, 50) 
    produtos_page = paginator.get_page(page)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  
        produtos_data = [
            {
                'id': produto.id,
                'name': produto.name,
                'price': produto.price,
                'images': produto.images,
                'farmacia': produto.nome_farmacia,
                'produto_url': f"/produto/{produto.name}/{produto.nome_farmacia}/"
            }
            for produto in produtos_page
        ]
        return JsonResponse({'produtos': produtos_data, 'has_next': produtos_page.has_next()})

    return render(request, 'busca_resultados.html', {'produtos': produtos_page, 'query': query})