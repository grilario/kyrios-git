from django.urls import path
from django.contrib.auth import views

from .views import register

urlpatterns = [
    path('login/', views.LoginView.as_view(template_name='accounts/login.html')),
    path('signup/', register, name='register'),
]
