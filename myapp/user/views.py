from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from .models import Profile
from .forms import RegisterForm, LoginForm, ProfileForm
# Create your views here.

### Register
class Registration(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('blog:list')
        form = RegisterForm()
        context = {
            'title':'User',
            'form':form
        }
        return render(request, 'user/user_register.html', context)
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            Profile.objects.create(user=user)
            return redirect('user:login')


### Login
class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('blog:list')
        form = LoginForm()
        context = {
            'form':form
        }
        return render(request, 'user/user_login.html', context)
    def post(self, request):
        if request.user.is_authenticated:
            return redirect('blog:list')
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            
            if user:
                login(request, user)
                return redirect('blog:list')
        context = {
            'fomr':form
        }
        return render(request, 'user/user_login.html', context)


### Logout
class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('blog:list')


### Profile
class ProfileView(View):
    def get(self, request):
        user_profile = Profile.objects.get(user=request.user)
        # user_profile = Profile.objects.all()
        form = ProfileForm(initial={
            'username': user_profile.user.username, 
            'name': user_profile.user.name,
            'business':user_profile.user.business, 
            'address':user_profile.user.address,
            'city':user_profile.user.city,
            'town':user_profile.user.town})
        context = {
            'user_profile': user_profile,
            'form' : form
            }
        return render(request, 'user/user_profile.html', context)



class Update(View):
    def get(self, request):
        # user_profile = Profile.objects.get(user=request.user)

        form = ProfileForm(instance=request.user)
        context = {
            'form':form,
            # 'user':user_profile
        }
        return render(request, 'user/user_edit.html', context)
    def post(self, request):
        form = ProfileForm(request.POST, instance=request.user)
        

        if form.is_valid():
            # profile = form.save(commit=False)
            # profile.user = request.user
            form.save()
            
            return redirect('user:profile')