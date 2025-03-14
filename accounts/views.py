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
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.tokens import default_token_generator
from .forms import ResetPasswordForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
# Create your views here.
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q, Count
from datetime import timedelta


# Função auxiliar para verificar se o usuário é admin
def is_admin(user):
    return user.is_staff or user.is_superuser

# Decorator para proteger as views do admin
def admin_required(view_func):
    decorated_view = login_required(user_passes_test(is_admin)(view_func))
    return decorated_view

@admin_required
def admin_dashboard(request):
    # Dados para o dashboard
    total_usuarios = AppUser.objects.count()
    total_casas = Casa.objects.count()
    
    # Usuários e casas dos últimos 30 dias
    data_limite = timezone.now() - timedelta(days=30)
    novos_usuarios = AppUser.objects.filter(date_joined__gte=data_limite).count()
    novas_casas = Casa.objects.filter(data_cadastro__gte=data_limite).count()
    
    # Usuários recentes (10 últimos)
    usuarios_recentes = AppUser.objects.order_by('-date_joined')[:10]
    
    # Casas recentes (10 últimas)
    casas_recentes = Casa.objects.order_by('-data_cadastro')[:10]
    
    context = {
        'active_tab': 'dashboard',
        'total_usuarios': total_usuarios,
        'total_casas': total_casas,
        'novos_usuarios': novos_usuarios,
        'novas_casas': novas_casas,
        'usuarios_recentes': usuarios_recentes,
        'casas_recentes': casas_recentes,
    }
    
    return render(request, 'admin/dashboard.html', context)

@admin_required
def admin_usuarios(request):
    # Busca de usuários
    search_query = request.GET.get('search', '')
    if search_query:
        usuarios = AppUser.objects.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(cpf__icontains=search_query)
        ).annotate(casas_count=Count('casa'))
    else:
        usuarios = AppUser.objects.all().annotate(casas_count=Count('casa'))
    
    # Paginação
    paginator = Paginator(usuarios, 15)  # 15 usuários por página
    page_number = request.GET.get('page')
    usuarios_paginados = paginator.get_page(page_number)
    
    context = {
        'active_tab': 'usuarios',
        'usuarios': usuarios_paginados,
        'search_query': search_query,
    }
    
    return render(request, 'admin/usuarios.html', context)

@admin_required
def admin_usuario_detalhes(request, user_id):
    usuario = get_object_or_404(AppUser, id=user_id)
    casas = Casa.objects.filter(owner=usuario)
    
    context = {
        'active_tab': 'usuarios',
        'usuario': usuario,
        'casas': casas,
    }
    
    return render(request, 'admin/usuario_detalhes.html', context)


@admin_required
def admin_casas(request):
    # Busca de casas
    search_query = request.GET.get('search', '')
    if search_query:
        casas = Casa.objects.filter(
            Q(titulo__icontains=search_query) |
            Q(endereco__icontains=search_query) |
            Q(owner__first_name__icontains=search_query) |
            Q(owner__last_name__icontains=search_query)
        )
    else:
        casas = Casa.objects.all()
    
    # Paginação
    paginator = Paginator(casas, 10)  # 10 casas por página
    page_number = request.GET.get('page')
    casas_paginadas = paginator.get_page(page_number)
    
    context = {
        'active_tab': 'casas',
        'casas': casas_paginadas,
        'search_query': search_query,
    }
    
    return render(request, 'admin/casas.html', context)

@admin_required
def admin_casa_detalhes(request, casa_id):
    casa = get_object_or_404(Casa, id=casa_id)
    
    context = {
        'active_tab': 'casas',
        'casa': casa,
    }
    
    return render(request, 'admin/casa_detalhes.html', context)

@admin_required
def admin_casa_editar(request, casa_id):
    casa = get_object_or_404(Casa, id=casa_id)
    
    if request.method == 'POST':
        # Atualizar os dados da casa
        casa.titulo = request.POST.get('titulo')
        casa.endereco = request.POST.get('endereco')
        casa.tipo = request.POST.get('tipo')
        casa.preco_mes = request.POST.get('preco_mes')
        casa.capacidade_máxima = request.POST.get('capacidade_maxima')
        casa.descricao = request.POST.get('descricao')
        casa.contato = request.POST.get('contato')
        
        # Processar imagem principal se enviada
        if 'imagem_principal' in request.FILES:
            casa.imagem_principal = request.FILES['imagem_principal']
        
        casa.save()
        messages.success(request, 'Casa atualizada com sucesso!')
        return redirect('admin_casa_detalhes', casa_id=casa.id)
    
    context = {
        'active_tab': 'casas',
        'casa': casa,
    }
    
    return render(request, 'admin/casa_editar.html', context)

@admin_required
def admin_casa_excluir(request, casa_id):
    casa = get_object_or_404(Casa, id=casa_id)
    
    if request.method == 'POST':
        casa.delete()
        messages.success(request, 'Casa excluída com sucesso!')
        return redirect('admin_casas')
    
    context = {
        'active_tab': 'casas',
        'casa': casa,
    }
    
    return render(request, 'admin/casa_excluir.html', context)






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
            user  = AppUser.objects.create_user(
                nome=nome,
                email=email,
                password=password,
                last_name=sobrenome,
                telefone=telefone,
                data_nascimento= data_nascimento,
                cpf=cpf,
            
            )
            user.full_clean()  # Validar todos os campos
                
                
            user.set_password(password)
                
                
            user.save()

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