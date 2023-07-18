from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django import forms
from .models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterForm(UserCreationForm):
    # address = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': '도/시/동 입력'}))
    
    class Meta:
        model = User
        fields = ['username','name', 'business','address','city','town']



class ProfileForm(UserChangeForm):
    password = None
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].disabled = True
        self.fields['business'].disabled = True
    class Meta:
        model = User
        fields = ['username','name', 'business','address','city','town']


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'business']


class PasswordForm(PasswordChangeForm):
    class Meta:
        model=User
        fields = ['password']