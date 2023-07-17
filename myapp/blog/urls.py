from django.urls import path
from . import views

app_name = 'blog'

urlpatterns =[
    path('', views.Index.as_view(), name='list'),
    path('detail/<int:pk>', views.DetailView.as_view(), name='detail'),
    path('write/', views.Write.as_view(), name='write'),
]