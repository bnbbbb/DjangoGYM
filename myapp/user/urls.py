from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    # 회원가입
    path('register/', views.Registration.as_view(), name = 'register'),
    # path('busiregister/', views.BusinessRegi.as_view(), name = 'busiregister'),
    path('login/', views.Login.as_view(), name = 'login'),
    path('logout/', views.Logout.as_view(), name = 'logout'),
    path('profile/', views.ProfileView.as_view(), name = 'profile'),
    path('edit/', views.Update.as_view(), name = 'edit'),
]