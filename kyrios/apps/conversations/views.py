from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed, HttpResponseNotFound
from django.shortcuts import redirect, render

from apps.tasks.forms import TaskForm
from apps.tasks.models import Task, Attachment
from apps.communities.models import Community, Member

@login_required
def create(request, communityID):
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

          for fileField in request.FILES:
            file = Attachment.objects.create(task=form.instance, filename=request.FILES[fileField].name, file=request.FILES[fileField])

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
    attachments = Attachment.objects.filter(task=task)

    context = {
      'task': task,
      'attachments': attachments
    }

    return render(request, 'tasks/detail.html', context)
  except:
    return HttpResponseNotFound()
    