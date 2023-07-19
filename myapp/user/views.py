from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import default_storage
from .models import Profile
from .forms import RegisterForm, LoginForm, ProfileForm, PasswordForm, ProfileImageForm
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
            'town':user_profile.user.town,
            # 'userprofile':user_profile.user.image
            })
        context = {
            'user_profile': user_profile,
            'form' : form
            }
        if user_profile.image:  # 이미지가 있는 경우에만 context에 추가합니다.
            context['profile_img'] = user_profile.image.url
        print(context)
        return render(request, 'user/user_profile.html', context)



class Update(View):
    def get(self, request):
        form = ProfileForm(instance=request.user)
        imgform = ProfileImageForm()
        context = {
            'form':form,
            'imgform':imgform,
            # 'user':user_profile
        }
        return render(request, 'user/user_edit.html', context)
    def post(self, request):
        form = ProfileForm(request.POST, instance=request.user)
        imgform = ProfileImageForm(request.POST,request.FILES)
        print(request.FILES)
        if form.is_valid() and imgform.is_valid():
            user = form.save(commit=False)
            user.save()
            profile = user.profile  # 연결된 Profile 인스턴스 가져오기
            if 'image' in request.FILES:  # 이미지가 새로 업로드된 경우
                # 기존 이미지 삭제
                if profile.image:  # 이미지가 존재하는지 확인
                    default_storage.delete(profile.image.path)  # 이미지 파일 삭제
                # 새 이미지 할당
                profile.image = imgform.cleaned_data['image']
            profile.save()  # Profile 모델 저장
            return redirect('user:profile')
        else:
            # 폼이 유효하지 않은 경우에 대한 처리 (예: 오류 메시지 표시)
            context = {
                'form': form,
                'imgform':imgform
            }
            return render(request, 'user/user_edit.html', context)


class Password(View):
    def get(self, request):
        form = PasswordForm(request.user)
        context = {
            'form':form
        }
        return render(request, 'user/user_password.html', context)
    def post(self, request):
        form = PasswordForm(request.user, request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('blog:list')
