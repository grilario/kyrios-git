from django.urls import path

from . import views

urlpatterns = [
    path('all/', view=views.list, name='listTasks'),
    path('create/', view=views.create, name='createTask'),
    path('<str:taskID>/', view=views.get, name='getTask'),
    path('<str:taskID>/send', view=views.send, name='sendTask'),
    # path('<uuid:taskID>/edit/', view=views.index, name='editTask'),
    # path('<uuid:taskID>/delete/', view=views.index, name='deleteTask'),
]
