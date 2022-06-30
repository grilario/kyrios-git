from django.urls import path

from . import views

urlpatterns = [
    path('create/', view=views.create, name='createTask'),
    path('<str:messageID>/', view=views.get, name='getTask'),
    path('<str:messageID>/edit/', view=views.edit, name='editTask'),
    path('<str:messageID>/delete/', view=views.delete, name='deleteTask'),
]