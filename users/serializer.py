# Profile Serializer
import re
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


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)

    # make these mutualy exclusive - user either provides email or phone number
    email = serializers.EmailField(required=False, allow_blank=True)
    mobile_number = serializers.CharField(required=False, allow_blank=True)

    
    class Meta:
        model = User
        fields = ['email', 'password', 'phone', 'mobile_number', 'role']
        extra_kwargs = {
            'role': {'required': True},
        }


    def validate_password2(self, attrs):
        # password matching validation
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Password don't match.")
        return attrs

        email = attrs.get('email', '').strip()
        mobile = attrs.get('mobile_number', '').strip()

        if not email and not mobile_number:
            raise serializers.ValidationError("Either email or mobile number is required.")

        if email and mobile:
            raise serializers.ValidationError("Either email or mobile number is required, not both.")
        

        # validate email
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return attrs

        # validate mobile number
        if User.objects.filter(mobile_number=mobile).exists():
            raise serializers.ValidationError("A user with this mobile number already exists.")
        return attrs

        if mobile:
            if not re.match(r'^[0-9]{10}$', mobile):
                raise serializers.ValidationError("Invalid mobile number.")
        return attrs

    
    def create(self, validated_data):
        password = validated_data.pop('password')

        if not validated_data.get('email'):
            validated_data['email'] = None

        
        user = User.objects.create_user(password=password, **validated_data)
        return user
        
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'phone', 'mobile_number', 'role']

    def validate_email(self, value):
        user = self.instance
        if User.objects.filter(email=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    
class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar', 'address']