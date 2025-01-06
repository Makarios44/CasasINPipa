from django.shortcuts import render

# Create your views here.

def reservas(request):
    return render(request,'reservas.html')