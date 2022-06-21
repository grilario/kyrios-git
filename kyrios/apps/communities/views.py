from django.http import Http404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Community

@login_required()
def getCommunity(request, communityID):
  try:
    community = Community.objects.get(pk=communityID)
    context = {
      'community': community
    }

    return render(request, 'communities/detail.html', context)
  except:
    raise Http404()