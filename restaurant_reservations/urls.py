from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views  # Import auth views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('reservations.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),  # Includes other auth URLs like password reset
]
