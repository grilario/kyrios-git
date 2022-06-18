from django.contrib import admin
from .models import Repository, RepositoryAccess, RepositoryStar, RepositoryTask

# Register your models here.
admin.site.register([Repository, RepositoryAccess, RepositoryStar, RepositoryTask])