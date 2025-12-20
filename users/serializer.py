from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, Profile


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for Profile model"""
    class Meta:
        model = Profile
        fields = ['id', 'bio', 'avatar', 'address', 'updated_at']
        read_only_fields = ['updated_at'] #  update_at is not editable


class UserSerializer(serializers.ModelSerializer):
    """Basic User serializer for listing and basic operations"""
    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'role', 'date_joined', 'is_active']
        read_only_fields = ['id', 'date_joined']


class UserDetailSerializer(serializers.ModelSerializer):
    """User serializer with nested profile"""
    profile = ProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'role', 'first_name', 'last_name', 
                  'date_joined', 'is_active', 'profile']
        read_only_fields = ['id', 'date_joined']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration with password validation"""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True, label='Confirm Password')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'phone', 'role', 
                  'first_name', 'last_name']
        extra_kwargs = {
            'email': {'required': True},
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
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user information"""
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'first_name', 'last_name']
        extra_kwargs = {
            'email': {'required': False},
        }
    
    def validate_email(self, value):
        user = self.instance
        if User.objects.filter(email=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating profile information"""
    class Meta:
        model = Profile
        fields = ['bio', 'avatar', 'address']

