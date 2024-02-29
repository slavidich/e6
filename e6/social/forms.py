from django import forms
from .models import *

class ChangeProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']