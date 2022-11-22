from django.db import models
from django.contrib.auth.models import AbstractUser
from phone_field import PhoneField


# User Table Schema: Each object of this class is an user record in the table
class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=31,blank=True)
    wallet = models.IntegerField(default=10000, blank=False)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []