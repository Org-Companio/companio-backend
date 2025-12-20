from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth import get_user_model, authenticate
from .serializer import UserRegistrationSerializer, UserDetailSerializer
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserRegisterView(GenericAPIView):
  serializer_class = UserRegistrationSerializer
  permission_classes = [permissions.AllowAny]

  def post(self, request, *args, **kwargs):
    user_serializer = self.get_serializer(data=request.data)
    if user_serializer.is_valid():
      user = user_serializer.save()
      refresh = RefreshToken.for_user(user)
      return Response({
        'message': 'User registered successfully',
        'user': UserDetailSerializer(user).data,
        'tokens': {
          'refresh': str(refresh),
          'access': str(refresh.access_token),
        }
      }, status=status.HTTP_201_CREATED)
    return Response({
      'message': 'User registration failed',
      'errors': user_serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(GenericAPIView):
  permission_classes = [permissions.AllowAny]

  def post(self, request, *args, **kwargs):
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
      return Response({
        'message': 'Email and password are required'
      }, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(request, username=email, password=password)
    
    if user is not None:
      refresh = RefreshToken.for_user(user)
      return Response({
        'message': 'Login successful',
        'user': UserDetailSerializer(user).data,
        'tokens': {
          'refresh': str(refresh),
          'access': str(refresh.access_token),
        }
      }, status=status.HTTP_200_OK)
    else:
      return Response({
        'message': 'Invalid email or password'
      }, status=status.HTTP_401_UNAUTHORIZED)


class UserProfileView(GenericAPIView):
  serializer_class = UserDetailSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request, *args, **kwargs):
    serializer = self.get_serializer(request.user)
    return Response({
      'user': serializer.data
    }, status=status.HTTP_200_OK)