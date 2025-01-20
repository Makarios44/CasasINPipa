from django.urls import path, include
from . import views
urlpatterns = [

path('login/', views.login, name='login'),
path('register/', views.register, name='register'),
path('perfil/',views.perfil, name='perfil'),
path('logout/',views.logout,name='logout'),
path('termos_de_uso/', views.termos_de_uso, name='termos_de_uso'),
path('editar-perfil/', views.editar_perfil, name='editar_perfil'),
]
