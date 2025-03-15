from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.models import AppUser
from bookings.models import Casa, ImagemAdicional
from bookings.forms import CasaForm
from accounts.forms import EditarPerfilForm


def is_superuser(user):
    return user.is_superuser


@login_required
@user_passes_test(is_superuser)
def admin_dashboard(request):
    return render(request, 'dashboard.html')  


# Views para Casas
@login_required
@user_passes_test(is_superuser)
def admin_casas_list(request):
    casas = Casa.objects.all()
    return render(request, 'casas_list.html', {'casas': casas}) 

@login_required
@user_passes_test(is_superuser)
def admin_casa_detail(request, casa_id):
    casa = get_object_or_404(Casa, id=casa_id)
    imagens = ImagemAdicional.objects.filter(casa=casa)
    return render(request, 'casa_detail.html', {'casa': casa, 'imagens': imagens}) 

@login_required
@user_passes_test(is_superuser)
def admin_casa_create(request):
    if request.method == 'POST':
        form = CasaForm(request.POST, request.FILES)
        if form.is_valid():
            casa = form.save(commit=False)
            casa.owner = request.user
            casa.save()
            return redirect('admin_casas_list')
    else:
        form = CasaForm()
    return render(request, 'casa_form.html', {'form': form}) 
@login_required
@user_passes_test(is_superuser)
def admin_casa_update(request, casa_id):
    casa = get_object_or_404(Casa, id=casa_id)
    if request.method == 'POST':
        form = CasaForm(request.POST, request.FILES, instance=casa)
        if form.is_valid():
            form.save()
            return redirect('admin_casas_list')
    else:
        form = CasaForm(instance=casa)
    return render(request, 'casa_form.html', {'form': form}) 

@login_required
@user_passes_test(is_superuser)
def admin_casa_delete(request, casa_id):
    casa = get_object_or_404(Casa, id=casa_id)
    if request.method == 'POST':
        casa.delete()
        return redirect('admin_casas_list')
    return render(request, 'casa_confirm_delete.html', {'casa': casa}) 


# Views para Usuários
@login_required
@user_passes_test(is_superuser)
def admin_users_list(request):
    users = AppUser.objects.all()
    return render(request, 'users_list.html', {'users': users})  

@login_required
@user_passes_test(is_superuser)
def admin_user_detail(request, user_id):
    user = get_object_or_404(AppUser, id=user_id)
    return render(request, 'user_detail.html', {'user': user}) 
@login_required
@user_passes_test(is_superuser)
def admin_user_update(request, user_id):
    user = get_object_or_404(AppUser, id=user_id)
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('admin_users_list')
    else:
        form = EditarPerfilForm(instance=user)
    return render(request, 'user_form.html', {'form': form})  

@login_required
@user_passes_test(is_superuser)
def admin_user_delete(request, user_id):
    user = get_object_or_404(AppUser, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('admin_users_list')
    return render(request, 'user_confirm_delete.html', {'user': user})  