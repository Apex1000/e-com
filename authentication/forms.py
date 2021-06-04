from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.forms import inlineformset_factory
from authentication.models import User
from django.contrib.auth.forms import UserCreationForm
from authentication import models as auth_models


class UsersForm(ModelForm):
    class Meta:
        model = User
        fields = "__all__"

class SignUpForm(UserCreationForm):
    phone_number = forms.IntegerField()
    email = forms.EmailField(max_length=200)
    
    class Meta:
        model = User
        fields = ("name", "email", "password1", "password2", "phone_number")
