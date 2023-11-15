from django.urls import path
from . import views

app_name = 'blog'

urlpatterns =[
    path('', views.List.as_view(), name='list'),
    path('detail/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('write/', views.Write.as_view(), name='write'),
    path('write/image/', views.PostImage.as_view(), name='write'),
    path('detail/<int:pk>/edit/', views.Update.as_view(), name='edit'),
    path('detail/<int:pk>/delete/', views.Delete.as_view(), name='delete'),
    # path("detail/<int:pk>/comment/write/", views.ReviewWrite.as_view(), name='rv-write'),
    # path("detail/comment/<int:pk>/delete/", views.ReviewDelete.as_view(), name='rv-delete'),
    path('search/<str:searchTerm>', views.SearchTag.as_view(), name='search'),
    # path('detail/<int:pk>/like/', views.LikePost.as_view(), name='like'),
]
