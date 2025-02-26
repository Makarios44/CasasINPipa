from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
path('',views.intro, name = 'intro'),
path('home', views.home, name='home'), #main 
path('rental/',views.rental, name='rental'),
path('editar/<int:casa_id>/', views.editar, name='editar'),
path('excluir-casa/<int:casa_id>/', views.excluir, name='excluir_casa'),
path('detalhes/<int:casa_id>/',views.detalhes, name='detalhes'),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)