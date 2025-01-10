from django.db import models

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

    def __str__(self):
        return self.nome
