from django.urls import path

from . import views

urlpatterns = [
    path('<str:communityID>/', views.getCommunity),
    # path('/<str:communityID>/members/'),
    # path('/<str:communityID>/tasks/'),
]


