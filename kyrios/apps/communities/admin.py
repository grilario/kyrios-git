from django.contrib import admin

from .models import Community, Member

admin.site.register([Community, Member])