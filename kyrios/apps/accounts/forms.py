from django.contrib.auth.forms import UserCreationForm

from apps.accounts.models import Account

class UserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Account
        fields =['picture', 'username', 'biography', 'password1', 'password2']