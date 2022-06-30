from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseNotAllowed
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect, render

from .forms import MessageForm
from apps.conversations.models import Message, Attachment
from apps.communities.models import Community, Member

@require_http_methods(['GET','POST'])
@login_required
def create(request, communityID):
  try:
    community = Community.objects.get(pk=communityID)
    member = Member.objects.get(account=request.user, community=community)

    if not member.isOrganizer:
      raise

    if request.POST:
      form = MessageForm(request.POST)
      
      if form.is_valid():
          form.instance.community = community
          form.instance.account = request.user
          form.save()

          for file in request.FILES.getlist('file'):
            Attachment.objects.create(message=form.instance, file=file)

          return redirect('/community/' + str(communityID))
  
    form = MessageForm()
    context = {
      'form': form,
      'communityID': str(communityID)
    }

    return render(request, 'messages/create.html', context)
  except:
    raise Http404()


@require_http_methods(['GET','POST'])
@login_required
def edit(request, communityID, messageID):
  try:
    message = Message.objects.get(pk=messageID)
    community = Community.objects.get(pk=communityID)
    member = Member.objects.get(account=request.user, community=community)

    if not member.isOrganizer:
      return HttpResponseNotAllowed()

    if request.POST:
      form = MessageForm(request.POST, instance=message)
      
      if form.is_valid():
          form.save()

          for file in request.FILES.values():
            Attachment.objects.create(message=form.instance, filename=file.name, file=file)

          return redirect('/community/' + str(communityID))
  
    form = MessageForm(instance=message)
    context = {
      'form': form,
      'communityID': str(communityID)
    }

    return render(request, 'messages/edit.html', context)
  except:
    raise Http404()


@require_http_methods(['GET'])
@login_required
def delete(request, communityID, messageID):
  try:
    message = Message.objects.get(pk=messageID)
    community = Community.objects.get(pk=communityID)
    member = Member.objects.get(account=request.user, community=community)

    if not member.isOrganizer:
      return HttpResponseNotAllowed()

    message.delete()

    return redirect('/community/' + communityID)
  except:
    raise Http404()


@require_http_methods(['GET'])
@login_required
def get(request, communityID, messageID):
  try:
    message = Message.objects.get(pk=messageID, community=communityID)
    attachments = Attachment.objects.filter(message=message)
    member = Member.objects.get(account=request.user, community=communityID)


    context = {
      'user': request.user,
      'message': message,
      'attachments': attachments,
      'isOrganizer': member.isOrganizer,
    }

    return render(request, 'messages/detail.html', context)
  except:
    raise Http404()