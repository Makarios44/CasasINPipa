from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login 
from django.contrib import messages

# Create your views here.
def login(request):
    if request.method == 'POST':
   
        nome = request.POST.get('login')
        password = request.POST.get('senha')

        usuario  = authenticate(username=nome, password=password)
        

        if usuario:
            auth_login(request, usuario)
            messages.success(request,'seja bem vindo')
            return  render(request,'reservas.html')
     
        else:
            messages.error(request,'email ou senha incorretos')
    
    return render(request,'login.html')

       


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    
    elif request.method == 'POST':
        # Captura os dados do formulário
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        password = request.POST.get('senha')
        password2 = request.POST.get('confirme_senha')
        telefone = request.POST.get('telefone')
        data_nascimento = request.POST.get('data_nascimento')

       
        if User.objects.filter(username=nome).exists():
            messages.error(request, 'Este usuario já está cadastrado')
        elif password != password2:
            messages.error(request, 'As senhas não são iguais')
        else:
            
            User.objects.create_user(
                username=nome, 
                email=email,
                password=password,
                last_name=sobrenome,
            )
            messages.success(request, 'Usuário cadastrado com sucesso')
            return render(request, 'login.html') 

    return render(request, 'register.html')




def perfil(request):
    return render(request,'perfil.html')