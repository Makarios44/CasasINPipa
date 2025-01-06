from django.shortcuts import render

# Create your views here.
def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    
    elif request.method == 'POST':
       
        return  render(request,'reservas.html')  
    

def register(request):
    if request.method == 'GET':
        return render(request,'register.html')
    
    elif request.method == 'POST':
         return render(request,'login.html')




def perfil(request):
    return render(request,'perfil.html')