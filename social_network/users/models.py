from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager


class User(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    email = models.EmailField(max_length=32, unique=True)
    last_activity = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email
