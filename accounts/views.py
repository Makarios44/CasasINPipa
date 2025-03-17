from django.shortcuts import render, redirect
from .models import AppUser
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
from django.urls import reverse

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
    # Armazenar os dados do formulário para reenchimento em caso de erro
    context = {}
    
    if request.method == 'POST':
        # Captura os dados do formulário
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        password = request.POST.get('senha')
        password2 = request.POST.get('confirme_senha')
        telefone = request.POST.get('telefone')
        cpf = request.POST.get('cpf')
        data_nascimento = request.POST.get('data_nascimento')
        termos = request.POST.get('termos')
        
        # Salvar os dados no contexto para reexibição em caso de erro
        context = {
            'nome': nome,
            'sobrenome': sobrenome,
            'email': email,
            'telefone': telefone,
            'cpf': cpf,
            'data_nascimento': data_nascimento,
        }
        
        # Lista para armazenar erros de cada campo
        field_errors = {}
        
        # Verificando email já existente
        if AppUser.objects.filter(email=email).exists():
            field_errors['email'] = 'Este email já está cadastrado'
        
        # Verificando senhas iguais
        if password != password2:
            field_errors['confirme_senha'] = 'As senhas não são iguais'
        
        # Verificando CPF válido usando a classe CPFField diretamente
        from django_cpf_cnpj.fields import CPFField
        try:
            # Criar uma instância temporária do campo CPF para validação
            cpf_field = CPFField()
            # Usar o método clean que aciona os validadores
            cpf_field.clean(cpf, None)
        except Exception as e:
            # Capturar a mensagem de erro original, se possível
            error_message = str(e)
            if "is not valid cpf" in error_message.lower():
                field_errors['cpf'] = f'CPF inválido. Por favor, verifique o formato.'
            else:
                field_errors['cpf'] = 'CPF inválido. Por favor, verifique o formato.'
        
        # Se não houver erros, criar o usuário
        if not field_errors:
            try:
                user = AppUser.objects.create_user(
                    email=email,
                    nome=nome,
                    password=password,
                    last_name=sobrenome,
                    telefone=telefone,
                    data_nascimento=data_nascimento,
                    cpf=cpf,
                )
                
                # Enviar o email de boas-vindas
                subject = "Seja bem-vindo à nossa plataforma!"
                message = f'Olá, {user.first_name}! Ficamos felizes em ver você por aqui. ' \
                          'Esperamos que nossa plataforma ajude você a alugar sua casa o mais rápido possível. ' \
                          'Abraços da nossa equipe :)'
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [user.email]
                send_mail(subject, message, from_email, recipient_list)
                
                messages.success(request, 'Usuário cadastrado com sucesso')
                return redirect('login')
            except Exception as e:
                # Log do erro para depuração
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Erro ao criar usuário: {str(e)}")
                
                # Mensagem genérica para o usuário
                messages.error(request, 'Ocorreu um erro ao processar seu cadastro. Por favor, tente novamente.')
        else:
            # Adicionar os erros ao contexto
            context['field_errors'] = field_errors
            
    return render(request, 'register.html', context)



@login_required
def perfil(request):
    casas = Casa.objects.filter(owner=request.user)  # Buscar apenas as casas do usuário sempre

    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=request.user)
        if form.is_valid():
            AppUser = form.save()

            # Atualiza a sessão caso a senha tenha sido alterada
            update_session_auth_hash(request, AppUser)

            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect('perfil')
    else:
        form = EditarPerfilForm(instance=request.user)

    return render(request, 'perfil.html', {'form': form, 'casas': casas,'AppUser': request.user})

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=request.user)  # Vincula ao usuário autenticado
        if form.is_valid():
            user = form.save()  
       
  
            # Envio do e-mail de atualização de perfil
            subject = "Sua conta foi atualizada!"
            message = f'Olá, {user.username}! Suas informações foram atualizadas com sucesso. ' \
                      'Se não foi você que fez essa mudança, entre em contato com nosso suporte Urgentemente!'
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


def Política_de_Privacidade(request):
    return render (request, 'Política_de_Privacidade.html')