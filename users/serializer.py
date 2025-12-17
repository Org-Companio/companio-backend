from rest_framework import serializers
from .models import Users

class UsersSerializer(serializers.Serializer):
  class Meta:
    models = Users
    fields = '__all__'


class ProfileSerializer(serializers.Serializer):
    class Meta:
        models = profile
        fields = '__all__'
