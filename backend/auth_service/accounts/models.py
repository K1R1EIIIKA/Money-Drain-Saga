from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    money = models.IntegerField(default=0)
