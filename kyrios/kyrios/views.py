from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from apps.accounts.models import Account
from apps.communities.models import Community, Member
from apps.tasks.models import Task

def index(request: HttpRequest):
  if not request.user.is_authenticated:
    return HttpResponse('Tururu')

  
  user = Account.objects.get(pk=request.user.id)
  communitiesID = Member.objects.filter(account=user).values_list('community')
  communities = Community.objects.filter(pk__in=communitiesID)
  tasks = Task.objects.filter(community__in=communitiesID)

  context = {
    'user': user,
    'communities': communities,
    'activities': tasks
  }

  return render(request, 'index.html', context)