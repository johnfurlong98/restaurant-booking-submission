from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('reservations.urls')),  # App-level URLs
    path('accounts/', include('django.contrib.auth.urls')),  # Login, logout, password reset
]
