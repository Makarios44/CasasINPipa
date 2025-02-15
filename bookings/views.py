from django.shortcuts import render, redirect,get_object_or_404
from .models import Casa, ImagemAdicional
from django.shortcuts import render
from .forms import CasaForm, ImagemAdicionalForm

from datetime import datetime
from django.contrib.auth.decorators import login_required

# Create your views here.
def reservas(request):
    casas = Casa.objects.all()  # Inicializa com todas as casas
    erro = None

    if request.method == 'GET':
        checkin = request.GET.get('checkin')
        checkout = request.GET.get('checkout')
        hospedes = request.GET.get('hospedes')

        # Verifique se os parâmetros são válidos
        if checkin and checkout and hospedes:
            try:
                # Converte as datas para o formato datetime.date
                checkin = datetime.strptime(checkin, '%Y-%m-%d').date()
                checkout = datetime.strptime(checkout, '%Y-%m-%d').date()
                hospedes = int(hospedes)

                # Filtra as casas com base nas datas e no número de hóspedes
                casas = Casa.objects.filter(
                    disponivel_de__lte=checkout,  # A casa deve estar disponível até a data de checkout
                    disponivel_ate__gte=checkin,  # A casa deve estar disponível desde a data de checkin
                    capacidade_maxima__gte=hospedes  # A casa deve ter capacidade para os hóspedes
                )

                # Verifica se há casas e, caso contrário, define a mensagem de erro
                if not casas:
                    erro = 'Não há casas disponíveis para essas datas e número de hóspedes.'
            except ValueError:
                erro = 'Formato de dados inválido.'
        

    return render(request, 'reservas.html', {'casas': casas, 'erro': erro})


@login_required
def rental(request):
    if request.method == 'POST':
        casa_form = CasaForm(request.POST, request.FILES)
        if casa_form.is_valid():
            # Salva a casa associando ao usuário logado
            casa = casa_form.save(commit=False)
            casa.owner = request.user
            casa.save()

            # Processa as imagens adicionais
            imagens_adicionais = request.FILES.getlist('imagens_adicionais')
            for imagem in imagens_adicionais:
                ImagemAdicional.objects.create(casa=casa, imagem=imagem)

            return redirect('reservas')  # Redireciona após o cadastro
    else:
        casa_form = CasaForm()

    return render(request, 'rental.html', {'casa_form': casa_form})


@login_required
def editar(request, casa_id):
    casa = get_object_or_404(Casa, id=casa_id)

    # Verificar se o usuário atual é o proprietário da casa
    if casa.owner != request.user:
        return redirect('reservas')

    if request.method == 'POST':
        # Atualizando os campos principais da casa
        casa.nome = request.POST['nome']
        casa.descricao = request.POST['descricao']
        casa.endereco = request.POST['endereco']
        casa.preco_diaria = request.POST['preco_diaria']
        casa.tipo = request.POST['tipo']
    
        imagem_principal = request.FILES.get('imagem_principal')  

        if imagem_principal:
            casa.imagem_principal = imagem_principal  




      
        imagens_adicionais = request.FILES.getlist('imagens_adicionais')
      
      
        if imagens_adicionais:
            casa.imagens_adicionais.all().delete()  
            for imagem in imagens_adicionais:
                casa.imagens_adicionais.create(imagem=imagem)  

        casa.save()
        return redirect('detalhes', casa_id=casa.id)  

    return render(request, 'editar.html', {'casa': casa})


@login_required
def excluir(request, casa_id):
    
    casa = get_object_or_404(Casa, id=casa_id)
    if casa.owner != request.user:
        return redirect('reservas')  

   
    if request.method == 'POST':
        casa.delete()  
        return redirect('reservas')  

    return render(request, 'confirmar_exclusao.html', {'casa': casa})

def detalhes(request, casa_id):
    casa = get_object_or_404(Casa, id=casa_id)
    return render(request, 'detalhes.html', {'casa': casa})