from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    is_admin   = models.BooleanField(default=False)
    is_nurse   = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
