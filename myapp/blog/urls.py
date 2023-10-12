from django.urls import path
from . import views

app_name = 'blog'

urlpatterns =[
    path('', views.List.as_view(), name='list'),
    # path('detail/<int:pk>', views.DetailView.as_view(), name='detail'),
    path('detail/', views.DetailView.as_view(), name='detail'),
    path('write/', views.Write.as_view(), name='write'),
    path('detail/<int:pk>/edit/', views.Update.as_view(), name='edit'),
    path('detail/<int:pk>/delete/', views.Delete.as_view(), name='delete'),
    path("detail/<int:pk>/comment/write/", views.ReviewWrite.as_view(), name='rv-write'),
    # detail/<int:pk> 글에 대한 id값
    # 코멘트 삭제
    path("detail/comment/<int:pk>/delete/", views.ReviewDelete.as_view(), name='rv-delete'),
    path("detal/<int:pk>/hashtag/write", views.TagWrite.as_view(), name = "tag-write"),
    # 태그 삭제
    path("detal/hashtag/<int:pk>/delete", views.TagDelete.as_view(), name = "tag-delete"),
    path('search/<str:tag>', views.SearchTag.as_view(), name='search'),
]
