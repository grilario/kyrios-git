from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpRequest, HttpResponseNotAllowed, HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from apps.tasks.forms import TaskForm
from apps.tasks.models import Task, Attachment
from apps.communities.models import Community, Member
from apps.repositories.models import Repository, RepositoryTask
from apps.accounts.models import Account
from apps.accounts.auth import base_auth
from git.action import GIT_ACTION_ADVERTISEMENT, GIT_ACTION_RESULT
from git.http import GitResponse
from git.repo import Repo


@require_http_methods(['GET','POST'])
@login_required
def create(request, communityID):
  try:
    community = Community.objects.get(pk=communityID)
    member = Member.objects.get(account=request.user, community=community)

    if not member.isOrganizer:
      raise

    if request.POST:
      form = TaskForm(request.POST)
      
      if form.is_valid():
          form.instance.community = community
          form.instance.account = request.user
          form.save()

          for file in request.FILES.getlist('file'):
            Attachment.objects.create(task=form.instance, file=file)

          return redirect('/community/' + str(communityID))
  
    form = TaskForm()
    context = {
      'form': form,
      'communityID': str(communityID)
    }

    return render(request, 'tasks/create.html', context)
  except:
    raise Http404()


@require_http_methods(['GET','POST'])
@login_required
def edit(request: HttpRequest, communityID, taskID):
  try:
    task = Task.objects.get(pk=taskID)
    community = Community.objects.get(pk=communityID)
    member = Member.objects.get(account=request.user, community=community)

    if not member.isOrganizer:
      return HttpResponseNotAllowed()

    if request.POST:
      form = TaskForm(request.POST, instance=task)
      
      if form.is_valid():
          form.save()

          for file in request.FILES.values():
            Attachment.objects.create(task=form.instance, filename=file.name, file=file)

          return redirect('/community/' + str(communityID))
  
    form = TaskForm(instance=task)
    context = {
      'form': form,
      'communityID': str(communityID)
    }

    return render(request, 'tasks/edit.html', context)
  except:
    raise Http404()


@require_http_methods(['GET'])
@login_required
def delete(request: HttpRequest, communityID, taskID):
  try:
    task = Task.objects.get(pk=taskID)
    community = Community.objects.get(pk=communityID)
    member = Member.objects.get(account=request.user, community=community)

    if not member.isOrganizer:
      return HttpResponseNotAllowed()

    task.delete()

    return redirect('/community/' + communityID)
  except:
    raise Http404()


@require_http_methods(['GET'])
@login_required
def list(request, communityID):
  try:
    community = Community.objects.get(pk=communityID)
    tasks = Task.objects.filter(community=community)

    context = {
      'tasks': tasks,
      'communityID': communityID
    }

    return render(request, 'tasks/list.html', context)

  except:
    raise Http404()


@require_http_methods(['GET'])
@login_required
def get(request, communityID, taskID):
  try:
    task = Task.objects.get(pk=taskID, community=communityID)
    attachments = Attachment.objects.filter(task=task)
    member = Member.objects.get(account=request.user, community=communityID)
    repositories = RepositoryTask.objects.filter(task=task).values_list('repository')
    accounts = Repository.objects.filter(pk__in=repositories).values_list('owner')
    shipments = Account.objects.filter(pk__in=accounts)


    context = {
      'user': request.user,
      'task': task,
      'attachments': attachments,
      'location': 'http://localhost:8000/community/{}/task/{}/'.format(communityID, taskID),
      'isOrganizer': member.isOrganizer,
      'shipments': shipments
    }

    return render(request, 'tasks/detail.html', context)
  except:
    raise Http404()


@require_http_methods(['GET'])
def get_info_refs(request: HttpRequest, communityID, taskID):
  if request.META.get('HTTP_AUTHORIZATION'):
    user = base_auth(request.META['HTTP_AUTHORIZATION'])
    if not user:
      return HttpResponseForbidden('Access forbidden.')
  else:
    res = HttpResponse()
    res.status_code = 401
    res['WWW-Authenticate'] = 'Basic'
    return res

  user = Account.objects.get(username=user)

  try:
    task = Task.objects.get(pk=taskID, community=communityID)
    community = Community.objects.get(pk=communityID)
    Member.objects.get(community=community, account=user)
  except:
      raise Http404()

  try:
      repo = Repository.objects.get(owner=user, name=taskID)
  except:
      repository = Repository.objects.create(name=taskID, description="", owner=user)
      task = Task.objects.get(pk=taskID)
      RepositoryTask.objects.create(task=task, repository=repository)


  requested_repo = Repo(Repo.get_repository_location(user.username, taskID))
  response = GitResponse(service=request.GET['service'], action=GIT_ACTION_ADVERTISEMENT,
                          repository=requested_repo, data=None)

  return response.get_http_info_refs()


@require_http_methods(['POST'])
@csrf_exempt
def service_rpc(request, communityID, taskID):
  try:
    if request.META.get('HTTP_AUTHORIZATION'):
      user = base_auth(request.META['HTTP_AUTHORIZATION'])
      if not user:
        return HttpResponseForbidden('Access forbidden.')
    else:
      res = HttpResponse()
      res.status_code = 401
      res['WWW-Authenticate'] = 'Basic'
      return res

    user = Account.objects.get(username=user)

    try:
      task = Task.objects.get(pk=taskID, community=communityID)
      community = Community.objects.get(pk=communityID)
      Member.objects.get(community=community, account=user)
    except:
      raise Http404()

    requested_repo = Repo(Repo.get_repository_location(user.username, taskID))
    response = GitResponse(service=request.path_info.split('/')[-1], action=GIT_ACTION_RESULT,
                            repository=requested_repo, data=request.body)

    return response.get_http_service_rpc()
  except:
    raise Http404()