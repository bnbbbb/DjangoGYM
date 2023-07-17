from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone

# Create your models here.

class UserManager(BaseUserManager):
    
    def _create_user(self, username, email, password, address, is_staff, is_superuser, **extra_fields):
        if not username:
            raise ValueError('Must have an usernae')
        now = timezone.localtime()
        user = self.model(
            username = username,
            email = email,
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
        return self._create_user(username, password, False, False, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        return self._create_user(username, password, True, True, **extra_fields)


class User(AbstractUser):
    username = models.CharField(unique=True, max_length=20)
    email = models.EmailField()
    name = models.CharField(max_length=10)
    is_staff = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    objects = UserManager()


class BusinessUser(User):
    
    business_code = models.CharField(max_length=40, unique=True)
    
    # USERNAME_FIELD = 'username'
    