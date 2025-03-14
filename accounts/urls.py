from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from . import admin_views
urlpatterns = [

path('login/', views.login, name='login'),
path('register/', views.register, name='register'),
path('perfil/',views.perfil, name='perfil'),
path('logout/',views.logout,name='logout'),
path('termos_de_uso/', views.termos_de_uso, name='termos_de_uso'),
path('editar-perfil/', views.editar_perfil, name='editar_perfil'),
path('Política_de_Privacidade/', views.Política_de_Privacidade, name='Política_de_Privacidade'),


path('admin-painel/', admin_views.admin_dashboard, name='admin_dashboard'),
path('admin-painel/usuarios/', admin_views.admin_usuarios, name='admin_usuarios'),
path('admin-painel/usuario/<int:user_id>/', admin_views.admin_usuario_detalhes, name='admin_usuario_detalhes'),
path('admin-painel/casas/', admin_views.admin_casas, name='admin_casas'),
path('admin-painel/casa/<int:casa_id>/', admin_views.admin_casa_detalhes, name='admin_casa_detalhes'),
path('admin-painel/casa/<int:casa_id>/editar/', admin_views.admin_casa_editar, name='admin_casa_editar'),
path('admin-painel/casa/<int:casa_id>/excluir/', admin_views.admin_casa_excluir, name='admin_casa_excluir'),




path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name='password_reset.html',
    ), name='reset_password'),

    
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_sent.html'
    ), name='password_reset_sent'),

    
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_form.html'
    ), name='password_reset_confirm'),

    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_done.html'
    ), name='password_reset_complete'),

    path('reset_password_done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'
    ), name='password_reset_done'),
]

