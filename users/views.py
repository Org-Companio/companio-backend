from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth import get_user_model
from .serializer import UsersSerializer

User = get_user_model()


class ListUsers(APIView):

  # View list of users
  authentication_classes = [authentication.TokenAuthentication]
  permission_classes = [permissions.IsAdminUser]
