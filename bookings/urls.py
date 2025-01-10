from django.urls import path, include
from . import views
urlpatterns = [

path('', views.reservas, name='reservas'),
path('rental/',views.rental, name='rental')

]
