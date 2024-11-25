from django.shortcuts import redirect
from django.contrib import messages
from core.models import CadastroModel

class PlanoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        public_paths = ["/", "/auth/", "/login/", "/logout/", "/card/", "/selecionar-plano/"] 

        if request.path in public_paths:
            return self.get_response(request)

        if request.user.is_authenticated:
            try:
                cadastro = CadastroModel.objects.get(id=request.user.id)
                plano = cadastro.plano
                consultas_restantes = cadastro.consultas_restantes

                if plano == 0:
                    messages.error(request, "Você precisa escolher um plano para continuar.")
                    return redirect('/#plans')

                elif plano == 1:  
                    if consultas_restantes <= 0:
                        messages.error(request, "Você atingiu o limite de acessos permitidos no plano Grátis.")
                        return redirect("core:index")
                    
                    if request.path in ["/main/", "/produto_detalhe/"]:
                        cadastro.consultas_restantes -= 1
                        cadastro.save()

                elif plano in [2, 3]:
                    pass

            except CadastroModel.DoesNotExist:
                messages.error(request, "Cadastro não encontrado. Faça login novamente.")
                return redirect("core:index") 

        return self.get_response(request)