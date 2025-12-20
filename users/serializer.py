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
        fields = ['id', 'email', 'phone', 'role', 'date_joined', 'is_active']
        read_only_fields = ['id', 'date_joined']

class UserDetailSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'role', 'date_joined', 'is_active', 'profile']
        read_only_fields = ['id', 'date_joined']


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'phone', 'role']
        extra_kwargs = {
            'email': {'required': True, 'unique': True},
            'role': {'required': True},
        }

        def validate(self, attrs):
            if attrs['password'] != attrs['password2']:
                raise serializers.ValidationError({"password": "Password fields didn't match."})
            return attrs
        
        def create(self, validated_data):
            validated_data.pop('password2')
            password = validated_data.pop('password')
            user = User.objects.create_user(password=password, **validated_data)
            Profile.objects.create(user=user)
            return user
        
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'phone', 'role']
        extra_kwargs = {
            'email': {'required': False},
        }

    def validate_email(self, value):
        user = self.instance
        if User.objects.filter(email=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    
class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar', 'address']