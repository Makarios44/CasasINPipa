from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [

path('', views.reservas, name='reservas'), #bookings
path('rental/',views.rental, name='rental'),
path('editar/<int:casa_id>/', views.editar, name='editar'),
path('excluir-casa/<int:casa_id>/', views.excluir, name='excluir_casa'),


]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)