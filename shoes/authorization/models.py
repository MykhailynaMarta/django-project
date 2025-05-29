from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from enum import Enum


class User_role(Enum):
    ADMIN = 'admin'
    USER = 'user'


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=100)
    user_role = models.CharField(choices=[(role.value, role.name) for role in User_role], editable=False,
                                 max_length=100, default=User_role.USER.value)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, editable=False)


def save(self, *args, **kwargs):
    if self.pk is not None:
        old_value_date_joined = CustomUser.objects.get(pk=self.pk).date_joined
        old_value_user_role = CustomUser.objects.get(pk=self.pk).user_role
        self.date_joined = old_value_date_joined
        self.user_role = old_value_user_role
    super(CustomUser, self).save(*args, **kwargs)


USERNAME_FIELD = 'username'
# objects = UserManager()
