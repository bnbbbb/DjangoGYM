from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    writer = models.CharField(max_length=20)
    # writer는 FK로 연결 해줌. 
    name = models.CharField(max_length=20)
    # image = models.ImageField(upload_to = 'blog/media/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
