from django.contrib import admin
from django.urls import path, include

from utils.server import serve
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('media/<str:filename>', serve),
    path('media/<str:uuid>/<str:filename>', serve),
    path('', include('apps.accounts.urls')),
    path('community/', include('apps.communities.urls')),
]
