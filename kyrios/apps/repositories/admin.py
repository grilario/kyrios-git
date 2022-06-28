from django.contrib import admin
from .models import Repository, RepositoryAccess, RepositoryTask

# Register your models here.
admin.site.register([Repository, RepositoryAccess, RepositoryTask])