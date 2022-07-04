from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from apps.accounts.models import Account

class UserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Account
        fields =['picture', 'username', 'biography']

class UserEditForm(UserChangeForm):
    class Meta(UserCreationForm.Meta):
        model = Account
        fields =['picture', 'username', 'biography']