from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import CadastroModel

class Command(BaseCommand):
    help = 'Apaga todos os usuários do banco de dados'

    def handle(self, *args, **kwargs):
        User.objects.all().delete()  # Apaga todos os usuários
        CadastroModel.objects.all().delete()  # Apaga todas as entradas do CadastroModel
        self.stdout.write(self.style.SUCCESS('Todos os usuários e cadastros foram apagados com sucesso!'))
