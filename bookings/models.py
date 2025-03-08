from django.db import models
from django.contrib.auth import get_user_model

AppUser = get_user_model()

class Casa(models.Model):
  
    descricao = models.TextField(null=False)
    endereco = models.CharField(max_length=255, null=False)
    preco = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    imagem_principal = models.ImageField(upload_to='casas/', null=True, blank=True)
    owner = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    capacidade_maxima = models.IntegerField(max_digits=10)
    contato =  models.CharField(max_length=15, help_text="Digite o número de telefone com DDD", default='0') 

    def __str__(self):
        return self.Localizacao


class ImagemAdicional(models.Model):
    casa = models.ForeignKey(Casa, related_name='imagens_adicionais', on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='imagens_adicionais/', null=False)

    def __str__(self):
        return f'Imagem adicional para {self.casa.nome}'