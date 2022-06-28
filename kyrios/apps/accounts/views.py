from django.shortcuts import redirect, render

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
  