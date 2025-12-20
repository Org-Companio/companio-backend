from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
  ROLE_CHOICES = (
      ('BOOKER', 'Booker'),
      ('COMPANION', 'Companion')
  )
  
  phone = models.CharField(max_length=20, unique=True, blank=True, null=True)
  email = models.EmailField(unique=True)
  role = models.CharField(max_length=20, choices=ROLE_CHOICES)
  date_joined = models.DateTimeField(auto_now_add=True)

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['role']

  def __str__(self):
      return f"{self.username} ({self.role})"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
