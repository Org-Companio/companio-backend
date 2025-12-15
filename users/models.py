from django.db import models
from djano.contrib.auth.models import AbstractUser

class Users (AbstractUser):
  ROLE_CHOICE = (
    ('BOOKER', 'booker'),
    ('COMPANION', 'companion')
  )
  phone = models.CharField(max_length=20, unique=True)
  email = models.CharField(max_length=20, unique=True)
  role = models.CharField(max_length=20, choice=ROLE_CHOICE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True) # updates the field evrytime sjango saves.
