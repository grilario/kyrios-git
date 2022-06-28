from django.forms.models import ModelForm

from .models import Community


class CommunityForm(ModelForm):
    class Meta:
        model = Community
        fields = ['picture', 'name', 'description']