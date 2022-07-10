from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.static import serve

from utils.server import serve as mediaServe
from . import views
from apps.accounts.views import edit

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('media/<str:filename>', mediaServe),
    path('media/<str:uuid>/<str:filename>', mediaServe),
    path('', include('apps.accounts.urls')),
    path('community/', include('apps.communities.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('search/', include('haystack.urls')),
    path('account', edit, name="profile"),
    path('static/<path:path>', serve, {'document_root': settings.STATIC_ROOT })
]


handler404 = 'kyrios.views.page_not_found'