from django.urls import path

from . import views

urlpatterns = [
    path('all/', view=views.list, name='listTasks'),
    path('<int:taskID>/', view=views.get, name='getTask'),
    path('create/', view=views.create, name='createTask'),
    # path('<uuid:taskID>/edit/', view=views.index, name='editTask'),
    # path('<uuid:taskID>/delete/', view=views.index, name='deleteTask'),
]
