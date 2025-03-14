from django.urls import path
from . import views


urlpatterns = [
    # URLs para Casas
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('casas/', views.admin_casas_list, name='admin_casas_list'),
    path('casas/<int:casa_id>/', views.admin_casa_detail, name='admin_casa_detail'),
    path('casas/create/', views.admin_casa_create, name='admin_casa_create'),
    path('casas/<int:casa_id>/update/', views.admin_casa_update, name='admin_casa_update'),
    path('casas/<int:casa_id>/delete/', views.admin_casa_delete, name='admin_casa_delete'),

    # URLs para Usuários
    path('users/', views.admin_users_list, name='admin_users_list'),
    path('users/<int:user_id>/', views.admin_user_detail, name='admin_user_detail'),
    path('users/<int:user_id>/update/', views.admin_user_update, name='admin_user_update'),
    path('users/<int:user_id>/delete/', views.admin_user_delete, name='admin_user_delete'),

]
