from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Article, Comment
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class AddPostForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['topic', 'image', 'description',]
        widgets = {
            'topic': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'floatingInputTopic',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'id': 'floatingInputImage',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'floatingInputDescription',
                'style': 'height: 100px;' 
            }),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Nazwa użytkownika'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Hasło'}))

class UpdateViewForm(forms.ModelForm):
    class Meta:
        model = Article 
        fields = ['topic', 'image', 'description']
        widgets = {
            'topic': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tytuł'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Opis'}),
        }