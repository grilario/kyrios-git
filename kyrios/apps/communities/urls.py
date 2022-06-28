from django.urls import path, include

from . import views

urlpatterns = [
    path('create/', view=views.createCommunity, name="createCommunity"),
    path('enter/', view=views.getCommunity, name="enterCommunity"),
    path('<str:communityID>/', view=views.getCommunity, name="getCommunity"),
    path('<str:communityID>/tasks', view=views.getCommunity, name="getTasks"),
    path('<str:communityID>/task/', include('apps.tasks.urls')),
    path('<str:communityID>/members/', view=views.getCommunity, name="listCommunityMembers"),
    path('<str:communityID>/edit/', view=views.editCommunity, name="editCommunity"),
    path('<str:communityID>/delete/', view=views.getCommunity, name="deleteCommunity"),
    path('<str:communityID>/task/', include('apps.tasks.urls'))
]
