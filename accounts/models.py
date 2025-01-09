from django.contrib.auth.models import AbstractUser
from django.db import models

class User:

    nome = models.CharField(max_length=50, null=False)
    sobrenome = models.CharField(max_length=50, null=False) 
    email = models.EmailField(max_length=254, null=False, unique=True)
    password = models.CharField( max_length=50)
    password2 = models.CharField( max_length=50)
    telefone = models.CharField(max_length=13, null=False)
    data_nascimento = models.DateField(null=False)
    
