from itertools import chain

from email.message import Message
from django.http import Http404, HttpRequest
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from apps.tasks.models import Task
from apps.conversations.models import Message
from apps.accounts.models import Account
from .models import Community, Member
from .forms import CommunityForm

@login_required()
def createCommunity(request):
  if request.POST:
    form = CommunityForm(request.POST, request.FILES)

    if form.is_valid():
      form.save()
      Member.objects.create(community=form.instance, account=request.user, isOrganizer=True, isOwner=True)
      
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
    messages = Message.objects.filter(community=community)
    member = Member.objects.get(community=community, account=request.user)

    activities = sorted(
    chain(tasks, messages),
    key=lambda instance: instance.created_at, reverse=True)

    context = {
      'community': community,
      'activities': activities,
      'isOrganizer': member.isOrganizer,
      'isOwner': member.isOwner
    }

    return render(request, 'communities/detail.html', context)
  except:
    raise Http404()

@login_required()
def editCommunity(request, communityID):
  try:
    community = Community.objects.get(pk=communityID)

    user = request.user
    member = Member.objects.get(account=user, community=community)

    if not member.isOrganizer:
      raise

    if request.POST:
      form = CommunityForm(request.POST, request.FILES, instance=community)

      if form.is_valid():
        form.instance.community = community
        form.save()
        
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
    member = Member.objects.get(account=user, community=community)

    if not member.isOrganizer:
      raise

    community.delete()

    return redirect('/')
  except:
    raise Http404()

def enterCommunity(request: HttpRequest):
  try:
    communityID = request.GET.get('communityID')
    community = Community.objects.get(pk=communityID)

    if request.headers.get('user-agent').__contains__('WhatsApp'):
      return render(request, 'communities/bot.html', { 'community': community })

    try:
      Member.objects.get(account=request.user, community=community)
      return redirect('getCommunity', communityID)
    except:
      Member.objects.create(account=request.user, community=community)
      return redirect('getCommunity', communityID)

    raise Http404()
  except:
    raise Http404()


@login_required()
def listMembers(request, communityID):
  try:
    community = Community.objects.get(pk=communityID)
    member = Member.objects.get(community=community, account=request.user)
    members = Member.objects.filter(community=community).order_by('-isOrganizer')

    context = {
      'community': community,
      'members': members,
      'isOrganizer': member.isOrganizer,
      'isOwner': member.isOwner
    }

    return render(request, 'communities/members.html', context)
  except:
    raise Http404()


@login_required()
def expulseMember(request, communityID, username):
  try:
    community = Community.objects.get(pk=communityID)
    member = Member.objects.get(community=community, account=request.user)
    accountToExpulse = Account.objects.get(username=username)
    memberToExpulse = Member.objects.get(account=accountToExpulse, community=community)

    if not member.isOrganizer or memberToExpulse.isOrganizer:
      raise Http404()
    
    memberToExpulse.delete()
    return redirect('listCommunityMembers', communityID=communityID)
  except:
    raise Http404()

@login_required()
def turnOrganizer(request, communityID, username):
  try:
    community = Community.objects.get(pk=communityID)
    member = Member.objects.get(community=community, account=request.user)
    accountToOrganizer = Account.objects.get(username=username)
    memberToOrganizer = Member.objects.get(account=accountToOrganizer, community=community)

    if not member.isOrganizer:
      raise Http404()
    
    if memberToOrganizer.isOwner or member.account == accountToOrganizer:
      raise Http404()
    
    if memberToOrganizer.isOrganizer:
      memberToOrganizer.isOrganizer = False
    else:
      memberToOrganizer.isOrganizer = True
    memberToOrganizer.save()

    return redirect('listCommunityMembers', communityID=communityID)
  except:
    raise Http404()

@login_required()
def leave(request, communityID):
  try:
    community = Community.objects.get(pk=communityID)
    member = Member.objects.get(community=community, account=request.user)

    if member.isOwner:
      raise Http404()
    
    member.delete()

    return redirect('/')
  except:
    raise Http404()