from django.shortcuts import render, redirect,get_object_or_404
from .models import Casa, ImagemAdicional
from django.shortcuts import render
from .forms import CasaForm, ImagemAdicionalForm

from datetime import datetime
from django.contrib.auth.decorators import login_required

from bookings.models import AppUser
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
def home(request):
    casas = Casa.objects.all()  # todas as casas
    erro = None
 
    return render(request, 'home.html', {'casas': casas, 'erro': erro})


@login_required
def rental(request):
    if request.method == 'POST':
        casa_form = CasaForm(request.POST, request.FILES)
        if casa_form.is_valid():
            casa = casa_form.save(commit=False)
            casa.owner = request.user
            casa.save()

            imagens_adicionais = request.FILES.getlist('imagens_adicionais')
            for imagem in imagens_adicionais:
                ImagemAdicional.objects.create(casa=casa, imagem=imagem)

           
            subject = "Sua casa foi cadastrada com sucesso!"
            message = f'Olá, {casa.owner.username}! Sua casa foi cadastrada com sucesso em nossa plataforma. ' \
                      'Ela está agora disponível para alugar. Obrigado por escolher nossa plataforma!'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [casa.owner.email]
            send_mail(subject, message, from_email, recipient_list)

            all_users = AppUser.objects.exclude(id=casa.owner.id)  # Todos os usuários, exceto o dono da casa
            subject_for_users = "Nova casa cadastrada!"
            message_for_users = f'Olá! Uma nova casa na "{casa.endereco}" foi cadastrada na plataforma. Confira agora!'

            recipient_list_for_users = all_users.values_list('email', flat=True)
            if recipient_list_for_users:
                send_mail(subject_for_users, message_for_users, from_email, recipient_list_for_users)


            return redirect('home') 
    else:
        casa_form = CasaForm()

    return render(request, 'rental.html', {'casa_form': casa_form})

@login_required
def editar(request, casa_id):
    casa = get_object_or_404(Casa, id=casa_id)

    
    if casa.owner != request.user:
        return redirect('home')

    if request.method == 'POST':
   
        
        casa.descricao = request.POST['descricao']
        casa.endereco = request.POST['endereco']
        casa.preco_diaria = request.POST['preco_diaria']
       
    
        imagem_principal = request.FILES.get('imagem_principal')  

        if imagem_principal:
            casa.imagem_principal = imagem_principal  

        imagens_adicionais = request.FILES.getlist('imagens_adicionais')
        if imagens_adicionais:
            casa.imagens_adicionais.all().delete()  
            for imagem in imagens_adicionais:
                casa.imagens_adicionais.create(imagem=imagem)

        casa.save()

       
        subject = "Sua casa foi atualizada!"
        message = f'Olá, {casa.owner.username}! As informações da sua casa foram atualizadas com sucesso. ' \
                  'Se você não fez essas alterações, entre em contato conosco.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [casa.owner.email]
        send_mail(subject, message, from_email, recipient_list)

        return redirect('detalhes', casa_id=casa.id)

    return render(request, 'editar.html', {'casa': casa})

@login_required
def excluir(request, casa_id):
    casa = get_object_or_404(Casa, id=casa_id)
    if casa.owner != request.user:
        return redirect('home')

    if request.method == 'POST':
        casa.delete()

     
        subject = "Sua casa foi excluída!"
        message = f'Olá, {casa.owner.username}! Sua casa foi excluída com sucesso da nossa plataforma. ' \
                  'Se você não solicitou essa exclusão, por favor, entre em contato conosco imediatamente.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [casa.owner.email]
        send_mail(subject, message, from_email, recipient_list)

        return redirect('home')

    return render(request, 'confirmar_exclusao.html', {'casa': casa})

def detalhes(request, casa_id):
    casa = get_object_or_404(Casa, id=casa_id)
    return render(request, 'detalhes.html', {'casa': casa})

def intro(request):
    return render (request,'intro.html')

def sobre_nos(request):
    return render (request ,'sobre_nos.html')