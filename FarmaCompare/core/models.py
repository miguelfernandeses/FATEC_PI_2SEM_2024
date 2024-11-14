from django.db import models
from django.contrib.auth.models import User


class CadastroModel(models.Model):
    email = models.EmailField('Email')
    razao_social = models.CharField(max_length=150, null=True, blank=True)
    cnpj = models.CharField(max_length=30, unique=True, null=True, blank=True)
    telefone = models.CharField(max_length=30, null=True, blank=True)
    endereco = models.CharField(max_length=255, null=True, blank=True)
    senha = models.CharField('Senha', max_length=50)
    

    def __str__(self):
        return self.razao_social
    
class Cliente(models.Model):
    razao_social = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=255)


class Plano(models.Model):
    PLANO_CHOICES = [
        (1, 'Grátis'),
        (2, 'Mensal'),
        (3, 'Anual'),
    ]

    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plano = models.IntegerField(choices=PLANO_CHOICES, default=1)
    data_assinatura = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_plano_display()}"
    
class Produto(models.Model):
    nome_farmacia = models.CharField(max_length=255)
    product_url = models.URLField(max_length=1024)
    ean = models.CharField(max_length=13, unique=False)  
    sku = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_old = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    substance = models.CharField(max_length=255, blank=True, null=True)
    factory = models.CharField(max_length=255, blank=True, null=True)
    brand = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    images = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ('ean', 'nome_farmacia')

    def __str__(self):
        return f"{self.name} - {self.nome_farmacia}"