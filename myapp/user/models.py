from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
from django.db.models.signals import post_save
from django.conf import settings

# Create your models here.

class UserManager(BaseUserManager):
    
    def _create_user(self, username, password, is_staff, is_superuser, **extra_fields):
        if not username:
            raise ValueError('Must have an username')
        now = timezone.localtime()
        user = self.model(
            username = username,
            # email = email,
            is_active = True,
            is_staff = is_staff,
            is_superuser = is_superuser,
            last_login = now,
            date_joined = now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        
        return user


    def create_superuser(self, username, password, **extra_fields):
        return self._create_user(username, password, True,True, True, **extra_fields)


class User(AbstractUser):
    username = models.CharField(unique=True, max_length=20)
    # email = None
    business = models.BooleanField(default=False)
    is_staff = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    objects = UserManager()


class Profile(models.Model):
    user = models.OneToOneField('User', on_delete = models.CASCADE)
    name = models.CharField(default='닉네임', max_length=10, null=True, blank=True)
    image = models.ImageField(upload_to='',blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    address_num = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    address_relate= models.CharField(max_length=100, blank=True, null=True)
    address_detail = models.CharField(max_length=100, blank=True, null=True)
    insta_url = models.TextField(blank=True, null=True)
    face_url = models.TextField(blank=True, null=True)
    twitter_url = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    
def on_post_save_for_user(sender, **kwargs):
    if kwargs['created']:
        user = kwargs['instance']
        Profile.objects.create(user=user)

post_save.connect(on_post_save_for_user, sender=settings.AUTH_USER_MODEL)