from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django_cpf_cnpj.fields import CPFField


class AppUserManager(BaseUserManager):
    def create_user(self, email, nome=None, password=None, **extra_fields):
        """Cria e retorna um usuário normal"""
        if not email:
            raise ValueError('O email é obrigatório')
        email = self.normalize_email(email)

        if self.model.objects.filter(email=email).exists():
            raise ValueError('Este email já está em uso')

        base_username = email.split('@')[0]  # Usa a parte antes do @ como base
        username = base_username
        counter = 1

        while self.model.objects.filter(username=username).exists():
            username = f"{base_username}_{counter}"
            counter += 1
        
        if not nome:
            nome = "Usuário"

        # Remove first_name de extra_fields para evitar duplicação
        extra_fields.pop("first_name", None)

        user = self.model(email=email, username=username, first_name=nome, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Cria e retorna um superusuário"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superusuário precisa ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superusuário precisa ter is_superuser=True.')

        return self.create_user(email, nome="SuperUser", password=password, **extra_fields)



class AppUser(AbstractUser):
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20)
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
