from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Article
from django import forms
class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        


class AddPostForm(forms.ModelForm):
    
    class Meta:
        model = Article
        fields = ['topic', 'image', 'description',]

