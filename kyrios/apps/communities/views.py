from django.http import Http404, HttpRequest
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from apps.tasks.models import Task

from .models import Community, Member
from .forms import CommunityForm

@login_required()
def createCommunity(request):
  if request.POST:
    form = CommunityForm(request.POST, request.FILES)

    if form.is_valid():
      form.save()
      Member.objects.create(community=form.instance, account=request.user, isOrganizer=True)
      
      return redirect('getCommunity', communityID=form.instance.id)
  
  form = CommunityForm()
  context = {
    'form': form
  }

  return render(request, 'communities/create.html', context)

@login_required()
def getCommunity(request, communityID):
  try:
    community = Community.objects.get(pk=communityID)
    tasks = Task.objects.filter(community=community)

    context = {
      'community': community,
      'activities': tasks
    }

    return render(request, 'communities/detail.html', context)
  except:
    raise Http404()

@login_required()
def editCommunity(request, communityID):
  try:
    community = Community.objects.get(pk=communityID)

    user = request.user
    member = Member.objects.get(account=user)

    if not member.isOrganizer:
      raise

    if request.POST:
      form = CommunityForm(request.POST, request.FILES, instance=community)

      if form.is_valid():
        form.save()
        Member.objects.create(community=form.instance, account=request.user, isOrganizer=True)
        
        return redirect('getCommunity', communityID=form.instance.id)
    
    form = CommunityForm(instance=community)
    context = {
      'form': form
    }

    return render(request, 'communities/edit.html', context)
  except:
    raise Http404()

@login_required()
def deleteCommunity(request, communityID):
  try:
    community = Community.objects.get(pk=communityID)

    user = request.user
    member = Member.objects.get(account=user)

    if not member.isOrganizer:
      raise

    community.delete()

    return redirect('/')
  except:
    raise Http404()

@login_required
def enterCommunity(request: HttpRequest):
  try:
    communityID = request.GET.get('communityID')
    community = Community.objects.get(pk=communityID)

    if Member.objects.filter(account=request.user):
      raise
    else:
      Member.objects.create(account=request.user, community=community)
      return redirect('getCommunity', communityID)

  except:
    raise Http404()