from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django import forms
from .models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterForm(UserCreationForm):
    # address = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': '도/시/동 입력'}))
    
    class Meta:
        model = User
        fields = ['username','name', 'business','address','city','town']


# class BusinessForm(UserCreationForm):
#     business = forms.BooleanField(required=False)
#     class Meta:
#         model = BusinessUser
#         fields = ['username', 'name','business']
# class ProfileForm(RegisterForm):
#     # username = forms.CharField(disabled=True)
#     # business = forms.BooleanField(disabled=True)
#     # address_choices = (('서울특별시', '서울특별시'), ('경기도', '경기도'), ('부산광역시', '부산광역시'), )
#     # address = forms.ChoiceField(choices=address_choices)
#     # city = forms.CharField(max_length=100)
#     # town = forms.CharField(max_length=100)
#     class Meta:
#         model = User
#         fields = RegisterForm.Meta.fields
class ProfileForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].disabled = True
        self.fields['business'].disabled = True
    class Meta:
        model = User
        fields = ['username','name', 'business','address','city','town']
        exclude = ['password']
        
class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'business']