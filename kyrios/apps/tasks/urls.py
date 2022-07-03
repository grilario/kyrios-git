from django.urls import path, include

from . import views

urlpatterns = [
    path('all/', view=views.listTasks, name='listTasks'),
    path('create/', view=views.create, name='createTask'),
    path('<str:taskID>/', view=views.get, name='getTask'),
    path('<str:taskID>/edit/', view=views.edit, name='editTask'),
    path('<str:taskID>/delete/', view=views.delete, name='deleteTask'),
    path('<str:taskID>/info/refs', views.get_info_refs, name='get_info_refs'),
    path('<str:taskID>/git-upload-pack', views.service_rpc, name='service_rpc'),
    path('<str:taskID>/git-receive-pack', views.service_rpc, name='service_rpc'),
    path('<str:repository>/<str:username>/', include('apps.repositories.urls'))
]
