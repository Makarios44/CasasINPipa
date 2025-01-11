from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.

from django.db import models

class Casa(models.Model):
    TIPOS_CASA = [
        ('Cs', 'Casa'),
        ('Apt', 'Apartamento'),
        ('Ch', 'Chalé'),
        ('St', 'Suíte'),
    ]

    nome = models.CharField(max_length=100, null=False)
    descricao = models.TextField(null=False)
    endereco = models.CharField(max_length=255, null=False)
    preco_diaria = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    disponivel = models.BooleanField(default=True)
    tipo = models.CharField(max_length=3, choices=TIPOS_CASA, null=False)
    imagem_principal = models.ImageField(upload_to='imagens_casas/', null=True, blank=True)

    def __str__(self):
        return self.nome
    
class ImagemAdicional(models.Model):
    casa = models.ForeignKey(Casa, related_name='imagens_adicionais', on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='imagens_adicionais/', null=False)
    
    def __str__(self):
        return f'Imagem adicional para {self.casa.nome}'
    
    def clean(self):
        if self.imagens_adicionais.count() > 7:
            raise ValidationError('Você não pode adicionar mais de 7 imagens adicionais.')