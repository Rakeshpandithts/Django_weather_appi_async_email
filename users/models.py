from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)

    # USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []



class weatherData(models.Model):
  timestamp = models.DateTimeField(auto_now_add=True)
  temperature = models.DecimalField(max_digits=12,decimal_places=2)
  description = models.CharField(max_length=150)
  city = models.CharField(max_length=150)

  def __str__(self):
    return "{}".format(self.timestamp)