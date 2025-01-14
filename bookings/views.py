from django.shortcuts import render, redirect,get_object_or_404
from .models import Casa, ImagemAdicional
from django.shortcuts import render

from django.contrib.auth.decorators import login_required

# Create your views here.

def reservas(request):
    casas = Casa.objects.all()
    print(casas) 
    return render(request, 'reservas.html', {'casas': casas})



@login_required
def rental(request):
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