from itertools import chain

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from apps.accounts.models import Account
from apps.communities.models import Community, Member
from apps.tasks.models import Task
from apps.conversations.models import Message

def index(request: HttpRequest):
  if not request.user.is_authenticated:
    return HttpResponse('Tururu')

  
  user = Account.objects.get(pk=request.user.id)
  communitiesID = Member.objects.filter(account=user).values_list('community')
  communities = Community.objects.filter(pk__in=communitiesID)
  tasks = Task.objects.filter(community__in=communitiesID)
  messages = Message.objects.filter(community__in=communitiesID)

  activities = sorted(
    chain(tasks, messages),
    key=lambda instance: instance.created_at, reverse=True)

  context = {
    'user': user,
    'communities': communities,
    'activities': activities
  }

  return render(request, 'index.html', context)