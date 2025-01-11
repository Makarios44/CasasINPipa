from django.shortcuts import render, redirect
from .models import Casa, ImagemAdicional

# Create your views here.

def reservas(request):

    casas = Casa.objects.all()

    return render(request,'reservas.html' ,{'casas':casas})

def rental(request):
    if  request.method  == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        endereco = request.POST.get('endereco')
        preco_diaria = request.POST.get('preco_diaria')
        tipo = request.POST.get('tipo')
        foto_principal = request.FILES.get('foto_principal')
        fotos_adicionais = request.FILES.getlist('fotos_adicionais') 

        casa = Casa.objects.create(
            nome=nome,
            descricao=descricao,
            endereco=endereco,
            preco_diaria=preco_diaria,
            tipo=tipo,
            imagem_principal=foto_principal
        )

         
        for foto in fotos_adicionais:
            ImagemAdicional.objects.create(casa=casa, imagem=foto)

        return redirect('bookings') 
    
    return render(request, 'rental.html')  

