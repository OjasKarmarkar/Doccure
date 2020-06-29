from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_doc = models.BooleanField(default=False)
    first_name = models.CharField(max_length=50 , default= 'User')
    age = models.IntegerField(default= 18)
    last_name = models.CharField(max_length=50 , default= 'User Surname')
    profession = models.CharField(max_length=50 , default= 'MD')
    address = models.CharField(max_length=200 , default= 'Mumbai , MH')
    city = models.CharField(max_length=200 , default= '')
    state = models.CharField(max_length=200 , default= '')
    phone = models.CharField(max_length=200 , default= '')
    bgroup = models.CharField(max_length=200 , default= '')
    photo = models.ImageField(upload_to='profilePic' , default = '')
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email