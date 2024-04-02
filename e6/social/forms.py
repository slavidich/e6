from django import forms
from django.core.exceptions import ValidationError

from .models import *

class ChangeProfile(forms.Form):
    firstname = forms.CharField(max_length=32, label='Имя', required=False)
    avatar = forms.ImageField(required=False, label='Аватар')
    bio = forms.CharField(required=False, label='О себе:', widget=forms.Textarea)

    def save(self, user):
        data = self.cleaned_data
        if data['firstname']:
            user.first_name = data['firstname']
        if data['avatar']:
            user.profile.avatar=data['avatar']
        elif data['avatar'] == False:
            user.profile.avatar = None
        if data['bio']:
            user.profile.bio = data['bio']
        user.save()
        user.profile.save()
    def clean_firstname(self):
        dicterror = {}
        firstname = self.cleaned_data.get('firstname')
        if not firstname.isalpha():
            raise ValidationError('Имя должно состоять только из букв')
        return firstname


class CreateRoom(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['roomname']