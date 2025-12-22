from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import permissions
from .serializer import UserDetailSerializer
from rest_framework import status


class UserProfileView(GenericAPIView):
  serializer_class = UserDetailSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request, *args, **kwargs):
    serializer = self.get_serializer(request.user)
    return Response({
      'user': serializer.data
    }, status=status.HTTP_200_OK)