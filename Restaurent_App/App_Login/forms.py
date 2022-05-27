
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

from .models import UserInfo


class UserForm(UserCreationForm):
    email = forms.EmailField(label='Email Address',required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)

class UserProfileChangeForm(UserChangeForm):
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileChangeForm_2(forms.ModelForm):
    
    class Meta:
        model = UserInfo
        fields = ('cell', 'address')

class ProfilePicForm(forms.ModelForm):

    class Meta:
        model = UserInfo
        fields = ['profile_pic']
