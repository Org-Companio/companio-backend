from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import UserRegisterView, UserLoginView, UserProfileView

urlpatterns = [
  path('register/', UserRegisterView.as_view(), name='user-register'),
  path('login/', UserLoginView.as_view(), name='user-login'),
  path('profile/', UserProfileView.as_view(), name='user-profile'),
  path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]