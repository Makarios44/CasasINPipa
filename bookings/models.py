from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
AppUser = get_user_model()


class Casa(models.Model):
    titulo = models.CharField(max_length=255, null=False, blank=True)  
    descricao = models.TextField(null=False)
    endereco = models.CharField(max_length=255, null=False)
    preco_mes = models.DecimalField(max_digits=10, decimal_places=0, null=False, default='0')  
    imagem_principal = models.ImageField(upload_to='casas/', null=True, blank=True)
    owner = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    contato = models.CharField(max_length=15, help_text="Digite o número de telefone com DDD", default='0')
    capacidade_máxima = models.DecimalField(max_digits=10, decimal_places=0, null=False, default='0')
    created_at = models.DateTimeField(default=timezone.now)
    

    # Características do imóvel
    numero_quartos = models.PositiveIntegerField(default=1)
    numero_banheiros = models.PositiveIntegerField(default=1)
    numero_suites = models.PositiveIntegerField(default=0)
    numero_vagas_garagem = models.PositiveIntegerField(default=0)
    mobiliado = models.BooleanField(default=False)
    aceita_pets = models.BooleanField(default=False)

    # Comodidades
    ar_condicionado = models.BooleanField(default=False)
    piscina = models.BooleanField(default=False)
    area_de_lazer = models.BooleanField(default=False)
    churrasqueira = models.BooleanField(default=False)
    wifi_incluido = models.BooleanField(default=False)
    energia_inclusa = models.BooleanField(default=False)
    agua_inclusa = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo



class ImagemAdicional(models.Model):
    casa = models.ForeignKey(Casa, related_name='imagens_adicionais', on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='imagens_adicionais/', null=False)

    def __str__(self):
        return f'Imagem adicional para {self.casa.id}'
    
class Videos(models.Model):
     casa = models.ForeignKey(Casa, related_name='videos', on_delete=models.CASCADE)
     video = models.FileField(upload_to='videos/', null=False)

