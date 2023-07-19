from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone

# Create your models here.

class UserManager(BaseUserManager):
    
    def _create_user(self, username, password, address, is_staff, is_superuser, **extra_fields):
        if not username:
            raise ValueError('Must have an usernae')
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

    def create_user(self, username, password, **extra_fields):
        return self._create_user(username, password, False,False, False, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        return self._create_user(username, password, True,True, True, **extra_fields)


class User(AbstractUser):
    username = models.CharField(unique=True, max_length=20)
    # email = None
    name = models.CharField(max_length=10)
    address_choices = (('서울특별시', '서울특별시'), ('경기도', '경기도'), ('부산광역시', '부산광역시'), )
    city = models.CharField(max_length=100)
    town = models.CharField(max_length=100)
    address = models.CharField(max_length=10, choices=address_choices)
    fulladdress = models.CharField(max_length=100)
    
    is_staff = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    business = models.BooleanField(default=False)
    objects = UserManager()
    
    def save(self, *args, **kwargs):
        self.fulladdress = f'{self.address} {self.city} {self.town}'
        super().save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField('User', on_delete = models.CASCADE)
    image = models.ImageField(upload_to = 'user/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)