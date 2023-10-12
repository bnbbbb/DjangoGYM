from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=40, blank=True)
    count = models.IntegerField(default = 0)
    thumbnail = models.ImageField(upload_to='blog/media',null=True,blank=True)
    image = models.ImageField(upload_to = 'blog/', blank=True, null=True)
    is_active = models.BooleanField(default = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    def save(self, *args, **kwargs):
        # User 모델로부터 필요한 정보 가져오기
        writer = self.writer  # Post 모델의 writer 필드는 User 객체를 참조합니다
        name = writer.name
        address = writer.address

        # 필요한 정보를 Post 모델에 할당
        self.name = name
        self.address = address

        super().save(*args, **kwargs)

class Review(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    content = models.TextField()
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    post = models.ForeignKey('Post', related_name='tags',on_delete=models.CASCADE)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    
    def __str__(self):
        return self.name