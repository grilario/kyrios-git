from django.urls import re_path

from .views import view_repository


urlpatterns = [
    re_path(r'tree/(?P<rev>[-\w]+)/*', view_repository, name='view_repository'),
    re_path(r'blob/(?P<rev>[-\w]+)/*', view_repository, name='view_repository'),
    re_path(r'$', view_repository, name='view_repository'),
]