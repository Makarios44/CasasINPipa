from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from bookings.models import Casa
from .forms import EditarPerfilForm
# Create your views here.
def login(request):

    if request.user.is_authenticated:
        return redirect('reservas') 

    if request.method == 'POST':
        nome = request.POST.get('login')
        password = request.POST.get('senha')
        usuario  = authenticate(username=nome, password=password)
        
        if usuario:
            auth_login(request, usuario)
        
            request.session['logado'] = True
            return  redirect('reservas')

        else:
            messages.error(request,'email ou senha incorretos')
            return  render(request,'login.html')
    
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
        terms = request.POST.get('terms')
        
        
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



@login_required
def perfil(request):
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()  # Salva as alterações feitas no usuário
            messages.success(request, "Informações do perfil atualizadas com sucesso!")
            return redirect('perfil')  # Redireciona para a página de perfil novamente
    else:
        form = EditarPerfilForm(instance=request.user)  # Carrega os dados atuais do usuário no formulário

    return render(request, 'perfil.html', {'form': form})



def editar_perfil(request):
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST)
        if form.is_valid():
            user = request.user
            user.first_name = form.cleaned_data['nome']
            user.last_name = form.cleaned_data['sobrenome']
            user.email = form.cleaned_data['email']
            if form.cleaned_data.get('senha'):
                user.set_password(form.cleaned_data['senha'])
            user.save()
            return redirect('perfil')  # Redireciona para a página de perfil

        else:
             form = EditarPerfilForm(instance=request.user)
         
    return render(request, 'perfil.html', {'form': form})




@login_required
def logout(request):
    auth_logout(request) 
    return redirect('login')

def termos_de_uso(request):
    return render(request, 'termos_de_uso.html')