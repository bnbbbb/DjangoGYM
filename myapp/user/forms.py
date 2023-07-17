from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import BusinessUser
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','name']


class BusinessForm(UserCreationForm):
    class Meta:
        model = BusinessUser
        fields = ['username', 'name','business_code']



class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']