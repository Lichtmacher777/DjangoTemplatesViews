from django import forms
from .models import User, Post
from django.contrib.auth.forms import AuthenticationForm


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'bio', 'age']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post', 'visibility']

class LoginForm(AuthenticationForm):  
    class Meta:
        model = User
        fields = ['username', 'password']