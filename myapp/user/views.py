from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm, BusinessForm
# Create your views here.

### Register
class Registration(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('blog:list')
        form = RegisterForm()
        context = {
            'form':form,
            'title':'User'
        }
        return render(request, 'user/user_register.html', context)
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('user:login')


class BusinessRegi(View):
    def get(self, request):
        form = BusinessForm()
        context = {
            'form':form
        }
        return render(request, 'user/business_register.html', context)
    def post(self, request):
        form = BusinessForm(request.POST)
        if form.is_valid():
            user = form.save()
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