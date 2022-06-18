from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseNotAllowed, HttpResponseNotFound
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from apps.tasks.forms import TaskForm
from apps.tasks.models import Task, Attachment
from apps.communities.models import Community, Member
from apps.repositories.models import Repository, RepositoryTask

@login_required
def create(request: HttpRequest, communityID):
  try:
    community = Community.objects.get(pk=communityID)
    member = Member.objects.get(account=request.user, community=community)

    if not member.isOrganizer:
      return HttpResponseNotAllowed()

    if request.POST:
      form = TaskForm(request.POST)
      
      if form.is_valid():
          form.instance.community = community
          form.save()

          for file in request.FILES.values():
            Attachment.objects.create(task=form.instance, filename=file.name, file=file)

          return redirect('/community/' + str(communityID))
  
    form = TaskForm()
    context = {
      'form': form,
      'communityID': str(communityID)
    }

    return render(request, 'tasks/create.html', context)
  except:
    return HttpResponseNotFound()


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
    return HttpResponseNotFound()

@login_required
def get(request, communityID, taskID):
  try:
    task = Task.objects.get(pk=taskID)

    if request.POST:
      repository = Repository.objects.create(name=task.title, owner=request.user)
      RepositoryTask.objects.create(task, repository)

    attachments = Attachment.objects.filter(task=task)

    context = {
      'task': task,
      'attachments': attachments
    }

    return render(request, 'tasks/detail.html', context)
  except:
    return HttpResponseNotFound()

@require_http_methods(['POST'])
@login_required
def send(request, communityID, taskID):
  # try:
    task = Task.objects.get(pk=taskID)

    if not RepositoryTask.objects.filter(task=task):
      repository = Repository.objects.create(name=task.title, owner=request.user)
      print('Hello')
      RepositoryTask.objects.create(task=task, repository=repository)

    return redirect(f'/community/{communityID}/task/{taskID}')
  # except:
  #   return HttpResponseNotFound()
    