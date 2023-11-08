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
from blog.upload import S3ImgUploader


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
        password = request.data['password']
        user = authenticate(username=id, password=password)
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
        profile = Pro.objects.get(user = request.user.id)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
        


class ProfileUpdate(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        profile = Pro.objects.get(user = request.user)
        request_data = request.data.copy()
        request_data['user'] = request.user.id
        delete_img = profile.image
        serializer = ProfileSerializer(profile, data=request_data)
        if serializer.is_valid():
            try:
                profileImage = request.FILES['image']
            except:
                exist_image = False
            else:
                exist_image = True
                
            if exist_image:
                delete_img = S3ImgUploader(delete_img)
                delete_img.delete()
                upload_img = S3ImgUploader(profileImage)
                upload_url = upload_img.upload('user')
                profile.image = upload_url
                profile.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePassword(APIView):
    def post(self, request):
        user = request.user
        print(user)
        cur_password = request.data.get('cur_password')
        new_password = request.data.get('new_password')
        if not user.check_password(cur_password):
            data = {
                'message' : '현재 비밀번호가 다릅니다.'
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        if user.check_password(new_password):
            data = {
                'message' : '현재 비밀번호와 변경할 비밀번호가 일치합니다.'
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()
        data = {
            'message':'비밀번호가 성공적으로 변경되었습니다.'
        }
        return Response(data, status=status.HTTP_200_OK)