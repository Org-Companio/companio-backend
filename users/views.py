from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.resonse import Response
from rest_framework import authenticaton, permisions
from django.contrib.auth.models import User
from .serializer import UsersSerializer


class ListUsers(APIView):

  # View list of users
  authenticaton_classes = [authenticaton.TokenAuthentication]
  permisions_classes = [permisions.IsAdminUser]


