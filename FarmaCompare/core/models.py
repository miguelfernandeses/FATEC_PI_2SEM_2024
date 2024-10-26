from django.db import models

class CadastroModel(models.Model):
    nome = models.CharField('Nome', max_length=200)
    email = models.EmailField('Email')
    senha = models.CharField('Senha', max_length=50)

    def __str__(self):
        return self.nome
    
class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=255)
    
    def __str__(self):
        return self.nome
    
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