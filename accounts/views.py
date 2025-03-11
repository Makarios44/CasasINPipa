from django.shortcuts import render, redirect
from .models import AppUser
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from bookings.models import Casa
from .forms import EditarPerfilForm
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.tokens import default_token_generator
from .forms import ResetPasswordForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
# Create your views here.



def login(request):

    if request.user.is_authenticated:
        return redirect('home') 

    if request.method == 'POST':
        email = request.POST.get('login')
        password = request.POST.get('senha')
        usuario  = authenticate(request, username=email, password=password)
        
        if usuario:
            auth_login(request, usuario)
        
            request.session['logado'] = True
            return  redirect('home')

        else:
            
            messages.error(request,'Email ou senha incorretos, tente novamente.')
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
        cpf = request.POST.get('cpf')
        data_nascimento = request.POST.get('data_nascimento')
        terms = request.POST.get('terms')

        if AppUser.objects.filter(email=email).exists():
            messages.error(request, 'Este email já está cadastrado')
        elif password != password2:
            messages.error(request, 'As senhas não são iguais')
        else:
            # Cria o usuário
            new_user = AppUser.objects.create_user(
                nome=nome,
                email=email,
                password=password,
                last_name=sobrenome,
                telefone=telefone,
                data_nascimento= data_nascimento,
                cpf=cpf,
            
            )
            new_user.full_clean()  # Validar todos os campos
                
                
            new_user.set_password(password)
                
                
            new_user.save()

            # Enviar o email de boas-vindas
            subject = "Seja bem-vindo à nossa plataforma!"
            message = f'Olá, {new_user.username}! Ficamos felizes em ver você por aqui. ' \
                      'Esperamos que nossa plataforma ajude você a alugar sua casa o mais rápido possível. ' \
                      'Abraços da nossa equipe :)'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [new_user.email]
            send_mail(subject, message, from_email, recipient_list)

            # Exibe uma mensagem de sucesso
            messages.success(request, 'Usuário cadastrado com sucesso')

            return render(request, 'login.html')

        
        
    return render(request, 'register.html')




@login_required
def perfil(request):
    casas = Casa.objects.filter(owner=request.user)  # Buscar apenas as casas do usuário sempre

    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=request.user)
        if form.is_valid():
            new_user = form.save()

            # Atualiza a sessão caso a senha tenha sido alterada
            update_session_auth_hash(request, new_user)

            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect('perfil')
    else:
        form = EditarPerfilForm(instance=request.user)

    return render(request, 'perfil.html', {'form': form, 'casas': casas, 'new_user': request.user})

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=request.user)  # Vincula ao usuário autenticado
        if form.is_valid():
            new_user = form.save()  
       
  
            # Envio do e-mail de atualização de perfil
            subject = "Sua conta foi atualizada!"
            message = f'Olá, {new_user.username}! Suas informações foram atualizadas com sucesso. ' \
                      'Se não foi você que fez essa mudança, entre em contato com nosso suport Urgentemente!'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [new_user.email]
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

@login_required    
def Password_reset(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            AppUser = AppUser.objects.filter(email=email).first()

            if AppUser:
                # Gerar o token e o uid para o link de reset
                token = default_token_generator.make_token(AppUser)
                uid = urlsafe_base64_encode(str(AppUser.pk).encode())


                # Construir o link de redefinição de senha
                reset_link = request.build_absolute_uri(f'/reset-password/{uid}/{token}/')

                # Preparar o e-mail
                subject = 'Redefinição de senha'
                message = render_to_string('password_reset_email.html', {
                    'reset_link': reset_link,
                    'AppUser': AppUser,
                })

                # Enviar o e-mail
                send_mail(subject, message, 'no-reply@meusite.com', [email])

                # Resposta de sucesso
                return HttpResponse("Instruções de recuperação de senha enviadas para seu e-mail.")
        else:
            if not AppUser:
              messages.error(request, "E-mail não encontrado no sistema.")
              return render(request, 'Password_reset.html', {'form': form})

    else:
        form = ResetPasswordForm()

    return render(request, 'Password_reset.html', {'form': form})

@login_required
def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        AppUser = AppUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, AppUser.DoesNotExist):
        AppUser = None

    if AppUser and default_token_generator.check_token(AppUser, token):
        if request.method == 'POST':
            form = SetPasswordForm(AppUser, request.POST)
            if form.is_valid():
                form.save()
                auth_login(request, AppUser)
                return redirect('home')  # Redirecionar para a página de login após redefinir
        else:
            form = SetPasswordForm(AppUser)
        
        return render(request, 'password_reset_confirm.html', {'form': form})
    else:
        return HttpResponse("O link de redefinição de senha é inválido ou expirou.")
    
def Política_de_Privacidade(request):
    return render (request, 'Política_de_Privacidade.html')