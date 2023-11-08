from django.db import models
from django.contrib.auth import get_user_model
from user.models import Profile
# Create your models here.

User = get_user_model()

class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=40, blank=True)
    count = models.IntegerField(default = 0)
    # thumbnail = models.ImageField(upload_to='blog/media',null=True,blank=True)
    # like_users = models.ManyToManyField(User, related_name='liked_posts')
    # image = models.ImageField(upload_to = 'blog/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class PostImage(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True)


class Review(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    content = models.TextField()
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    post = models.ForeignKey('Post', related_name='tags',on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    
