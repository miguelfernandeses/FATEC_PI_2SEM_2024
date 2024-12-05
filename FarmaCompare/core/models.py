from django.db import models
from django.contrib.auth.models import User

class CadastroModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(unique=True)
    razao_social = models.CharField(max_length=150, null=True, blank=True)
    cnpj = models.CharField(max_length=30, unique=True, null=True, blank=True)
    telefone = models.CharField(max_length=30, null=True, blank=True)
    endereco = models.CharField(max_length=255, null=True, blank=True)
    senha = models.CharField('Senha', max_length=50)
    plano = models.IntegerField(
        choices=[
            (0, 'Nenhum'),
            (1, 'Grátis'),
            (2, 'Mensal'),
            (3, 'Anual')
        ],
        default=0
    )

    consultas_restantes = models.IntegerField(default=10)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.razao_social or self.email
    
    
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