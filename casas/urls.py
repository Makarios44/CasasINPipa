from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('bookings/', include('bookings.urls')),
    path('notificatios/', include('notifications.urls')),
    path('payments/', include('payments.urls')),
    path('reviews/', include('reviews.urls')),

]
