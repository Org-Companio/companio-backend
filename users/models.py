from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):  # ← Also change 'Users' to 'User'
  
  ROLE_CHOICES = (
      ('BOOKER', 'Booker'),
      ('COMPANION', 'Companion')
  )
  
  phone = models.CharField(max_length=20, unique=True, blank=True, null=True)
  email = models.EmailField(unique=True)
  role = models.CharField(max_length=20, choices=ROLE_CHOICES)  # ← FIXED: 'choices'
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
      return f"{self.username} ({self.role})"