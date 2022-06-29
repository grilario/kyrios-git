from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from apps.accounts.forms import UserForm

def register(request):
  if request.POST:
    form = UserForm(request.POST, request.FILES)

    if form.is_valid():
      form.save()

      return redirect('/')
  
  form = UserForm()
  context = {
    'form': form
  }

  return render(request, 'accounts/register.html', context)

@login_required
def edit(request):
  if request.POST:
    form = UserForm(request.POST, request.FILES, instance=request.user)

    if form.is_valid():
      form.save()

      return redirect('/')
  
  form = UserForm(instance=request.user)
  context = {
    'form': form
  }

  return render(request, 'accounts/edit.html', context)
  