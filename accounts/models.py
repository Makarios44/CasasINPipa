from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django_cpf_cnpj.fields import CPFField



class AppUserManager(BaseUserManager):
    def create_user(self, email, nome, password=None, **extra_fields):
        if not email:
            raise ValueError('O email é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, first_name=nome, **extra_fields)
        user.set_password(password)  
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, nome, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, nome, password, **extra_fields)

class AppUser(AbstractUser):
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=13)
    data_nascimento = models.DateField(null=True)
   
    cpf = CPFField(
        null=True, 
        blank=False,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']
    
    objects = AppUserManager()
    
    def __str__(self):
        return self.email