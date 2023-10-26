from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import default_storage
# from .forms import RegisterForm, LoginForm, ProfileForm, PasswordForm, ProfileImageForm
# Create your views here.

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from .serializers import UserSerializer, ProfileSerializer
from user.models import User, Profile as Pro
from .tokens import create_jwt_pair_for_user


### Register
class Registration(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(is_active=True)
            data = {
                "message": "회원가입",
                "data" : serializer.data,
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            errors = serializer.errors
            data = {
                'error' : errors,
                'message' : '중복된 아이디가 있습니다. '
            }
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        

### Login
class Login(APIView):
    def post(self, request):
        id = request.data['username']
        # print(id)
        password = request.data['password']
        user = authenticate(username=id, password=password)
        # profile = ProfileSerializer(user=user)
        profile = Pro.objects.get(user= user.id)
        if user is not None:
            token = create_jwt_pair_for_user(user)
            serializer = UserSerializer(user)
            profileseri = ProfileSerializer(profile)
            data = {
                'Message' : '로그인',
                'token' : token,
                'user' : serializer.data,
                'profile': profileseri.data
            }
            return Response(data, status=status.HTTP_200_OK)
            
        else:
            # 사용자가 인증되지 않은 경우에도 Response를 반환해야 합니다.
            return Response({'Message': '로그인 실패'}, status=status.HTTP_401_UNAUTHORIZED)


### Logout
class Logout(View):
    def get(self, request):
        logout(request)
        return Response({'message': '로그아웃에 성공하였습니다.'}, status=status.HTTP_200_OK)


### Profile
class Profile(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # post = Profile.objects.get(id=request.data['post_id'])
        # user = 
        # user = Profile.objects.get()
        profile = Pro.objects.get(user = request.user.id)
        serializer = ProfileSerializer(profile)
        # print(serializer)
        # if serializer.is_valid():
            # serializer.save()
            
            # try:
            #     image = request.FILES('profileImage')
            # except:
            #     is_image = False
            # else:
            #     is_image = True
            # if is_image:
            #     user_profile.save()
                
        return Response(serializer.data, status=status.HTTP_200_OK)
        
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileUpdate(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        profile = Pro.objects.get(user = request.user)
        request_data = request.data.copy()
        request_data['user'] = request.user.id
        serializer = ProfileSerializer(profile, data=request_data)

        if serializer.is_valid():
            serializer.save()
            
            # try:
            #     image = request.FILES['profileImage']
            # except:
            #     is_image = False
            # else:
            #     is_image = True
                
            # if is_image:
            #     # img_uploader = S3ImgUploader(image)
            #     # uploaded_url = img_uploader.upload()
            #     # user_profile.profileImage = uploaded_url
            #     user_profile.save()
            # user_serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# class ProfileView(View):
#     def get(self, request):
        # user_profile = Profile.objects.get(user=request.user)
#         # user_profile = Profile.objects.all()
#         form = ProfileForm(initial={
#             'username': user_profile.user.username, 
#             'name': user_profile.user.name,
#             'business':user_profile.user.business, 
#             'address':user_profile.user.address,
#             'city':user_profile.user.city,
#             'town':user_profile.user.town,
#             # 'userprofile':user_profile.user.image
#             })
#         context = {
#             'user_profile': user_profile,
#             'form' : form
#             }
#         if user_profile.image:  # 이미지가 있는 경우에만 context에 추가합니다.
#             context['profile_img'] = user_profile.image.url
#         # print(context)
#         return render(request, 'user/user_profile.html', context)



# class Update(View):
#     def get(self, request):
#         form = ProfileForm(instance=request.user)
#         imgform = ProfileImageForm()
#         context = {
#             'form':form,
#             'imgform':imgform,
#             # 'user':user_profile
#         }
#         user_profile = Profile.objects.get(user=request.user)
#         if user_profile.image:  # 이미지가 있는 경우에만 context에 추가합니다.
#             context['profile_img'] = user_profile.image.url
#         return render(request, 'user/user_edit.html', context)
#     def post(self, request):
#         form = ProfileForm(request.POST, instance=request.user)
#         imgform = ProfileImageForm(request.POST,request.FILES)
#         # print(request.FILES)
#         if form.is_valid() and imgform.is_valid():
#             user = form.save(commit=False)
#             user.save()
#             profile = user.profile  # 연결된 Profile 인스턴스 가져오기
#             if 'image' in request.FILES:  # 이미지가 새로 업로드된 경우
#                 # 기존 이미지 삭제
#                 if profile.image:  # 이미지가 존재하는지 확인
#                     default_storage.delete(profile.image.path)  # 이미지 파일 삭제
#                 # 새 이미지 할당
#                 profile.image = imgform.cleaned_data['image']
#             profile.save()  # Profile 모델 저장
#             return redirect('user:profile')
#         else:
#             # 폼이 유효하지 않은 경우에 대한 처리 (예: 오류 메시지 표시)
#             context = {
#                 'form': form,
#                 'imgform':imgform
#             }
#             return render(request, 'user/user_edit.html', context)


# class Password(View):
#     def get(self, request):
#         form = PasswordForm(request.user)
#         context = {
#             'form':form
#         }
#         return render(request, 'user/user_password.html', context)
#     def post(self, request):
#         form = PasswordForm(request.user, request.POST)
        
#         if form.is_valid():
#             form.save()
#             return redirect('blog:list')
