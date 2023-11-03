from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    # 회원가입
    path('register/', views.Registration.as_view(), name = 'register'),
    # path('busiregister/', views.BusinessRegi.as_view(), name = 'busiregister'),
    path('login/', views.Login.as_view(), name = 'login'),
    path('logout/', views.Logout.as_view(), name = 'logout'),
    path('profile/', views.Profile.as_view(), name = 'profile'),
    path('profile/update/', views.ProfileUpdate.as_view(), name = 'profile'),
    path('password/', views.ChangePassword.as_view(), name = 'password'),
    # path('edit/', views.Update.as_view(), name = 'edit'),
    # path('password/', views.Password.as_view(), name = 'password'),
]