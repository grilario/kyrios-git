from django.contrib import admin
from django.shortcuts import render
from django.urls import path

from utils.server import serve

from apps.repositories.forms import RepositoryCreationForm

def index(request):
    return render(request, 'test.html', { 'form': RepositoryCreationForm() })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('media/<str:filename>', serve),
    path('media/<str:uuid>/<str:filename>', serve),
    path('', index)
]


