from django.shortcuts import render
from rest_framework.views import APIView, GenericAPIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth import get_user_model
from .serializer import UsersSerializer
from rest_framework import status

class UserRegisterView(GenericAPIView):
  serializer_class = UsersSerializer
  permission_classes = [permissions.AllowAny]

  def post(self, request, *args, **kwargs):
    user_serializer = self.get_serializer(data=request.data)
    if user_serializer.is_valid():
      user_serializer.save()
      return Response({
        'message': 'User registered successfully',
        'user': user_serializer.data
      }, status=status.HTTP_201_CREATED)
    return Response({
      'message': 'User registration failed',
      'errors': user_serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)