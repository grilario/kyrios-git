from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from apps.accounts.models import Account
from apps.communities.models import Community, Member

def index(request: HttpRequest):
  if not request.user.is_authenticated:
    return HttpResponse('Tururu')

  
  user = Account.objects.get(pk=request.user.id)
  communitiesID = Member.objects.filter(account=user).values_list('community')
  communities = Community.objects.filter(pk__in=communitiesID)

  context = {
    'user': user,
    'communities': communities
  }

  return render(request, 'index.html', context)