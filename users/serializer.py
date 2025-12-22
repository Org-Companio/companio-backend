# Profile Serializer
from rest_framework import serializers
from .models import Profile, User


class ProfileSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Profile
        fields = ['id', 'bio', 'avatar', 'address', 'updated_at']
        read_only_fields = ['updated_at'] 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'mobile_number', 'role', 'date_joined', 'is_active']
        read_only_fields = ['id', 'date_joined']

class UserDetailSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'mobile_number', 'role', 'date_joined', 'is_active', 'profile']
        read_only_fields = ['id', 'date_joined']

        
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'phone', 'mobile_number', 'password2', 'role']

    def validate_email(self, value):
        user = self.instance
        if User.objects.filter(email=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    
class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar', 'address']