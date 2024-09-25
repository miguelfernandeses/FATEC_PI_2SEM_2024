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
