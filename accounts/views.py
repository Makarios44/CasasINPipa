from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from bookings.models import Casa
from .forms import EditarPerfilForm
from django.contrib.auth import update_session_auth_hash

from django.conf import settings
from django.core.mail import send_mail
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

       
# views.py
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.conf import settings

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
            messages.error(request, 'Este usuário já está cadastrado')
        elif password != password2:
            messages.error(request, 'As senhas não são iguais')
        else:
            # Cria o usuário
            user = User.objects.create_user(
                username=nome,
                email=email,
                password=password,
                last_name=sobrenome,
            )

            # Enviar o email de boas-vindas
            subject = "Seja bem-vindo à nossa plataforma!"
            message = f'Olá, {user.username}! Ficamos felizes em ver você por aqui. ' \
                      'Esperamos que nossa plataforma ajude você a alugar sua casa o mais rápido possível. ' \
                      'Abraços da nossa equipe :)'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list)

            # Exibe uma mensagem de sucesso
            messages.success(request, 'Usuário cadastrado com sucesso')

            return render(request, 'login.html')

    return render(request, 'register.html')




@login_required
def perfil(request):
    casas = Casa.objects.filter(owner=request.user)  # Buscar as casas do usuário sempre

    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()

            # Atualiza a sessão caso a senha tenha sido alterada
            update_session_auth_hash(request, user)

            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect('perfil')
    else:
        form = EditarPerfilForm(instance=request.user)

    return render(request, 'perfil.html', {'form': form, 'casas': casas, 'user': request.user})

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=request.user)  # Vincula ao usuário autenticado
        if form.is_valid():
            user = request.user
            user.first_name = form.cleaned_data['nome']
            user.last_name = form.cleaned_data['sobrenome']
            user.email = form.cleaned_data['email']
            
            # Se o usuário alterou a senha
            if form.cleaned_data.get('senha'):
                user.set_password(form.cleaned_data['senha'])
            
            # Salva as alterações no perfil do usuário
            user.save()

            # Envio do e-mail de atualização de perfil
            subject = "Sua conta foi atualizada!"
            message = f'Olá, {user.username}! Suas informações foram atualizadas com sucesso. ' \
                      'Caso tenha feito alguma alteração, ela já está refletida em nossa plataforma.'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list)

            # Exibe uma mensagem de sucesso
            messages.success(request, 'Perfil atualizado com sucesso')

            return redirect('perfil')  # Redireciona para a página de perfil após salvar
    else:
        form = EditarPerfilForm(instance=request.user)  # Preenche o formulário com os dados do usuário

    return render(request, 'perfil.html', {'form': form})




@login_required
def logout(request):
    auth_logout(request) 
    return redirect('login')

def termos_de_uso(request):
    return render(request, 'termos_de_uso.html')

