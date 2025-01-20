from django.shortcuts import render, redirect,get_object_or_404
from .models import Casa, ImagemAdicional
from django.shortcuts import render


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
def rental(request): #cadastro de casas
    if request.method == 'POST':
      
        user = request.user  

        
        casa_obj = Casa.objects.create(
            nome=request.POST['nome'],
            descricao=request.POST['descricao'],
            endereco=request.POST['endereco'],
            preco_diaria=request.POST['preco_diaria'],
            tipo=request.POST['tipo'],
            imagem_principal=request.FILES['foto_principal'],
            owner=user 
        )
        
        return redirect('reservas')
    
    return render(request, 'rental.html')



@login_required
def editar(request, casa_id):
    casa = get_object_or_404(Casa, id=casa_id)

    
    if casa.owner != request.user:
        return redirect('reservas') 
    
    if request.method == 'POST':
        
        casa.nome = request.POST['nome']
        casa.descricao = request.POST['descricao']
        casa.endereco = request.POST['endereco']
        casa.preco_diaria = request.POST['preco_diaria']
        casa.tipo = request.POST['tipo']

        if 'imagem_principal' in request.FILES:
            casa.imagem_principal = request.FILES['imagem_principal']

        casa.save()
        return redirect('reservas')  # Redireciona após salvar

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

