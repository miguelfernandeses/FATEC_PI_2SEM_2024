from datetime import datetime
from .models import Cliente

class CadastroClienteService:
    def cadastrar_cliente(
        self, nome: str, email: str, senha: str,) -> dict:
        try:
            cliente = Cliente.objects.create(
                nome=nome,
                email=email,
                senha=senha,
            )
            return {"success": "Cliente cadastrado com sucesso."}
        except Exception as e:
            return {"error": str(e)}
        
