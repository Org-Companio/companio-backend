import re
from rest_framework import serializers
from users.models import User
from django.db.models import UniqueConstraint
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
MOBILE_REGEX = r'^[0-9]{10}$|^[+][0-9]{12}$'


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, allow_blank=False)
    password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = User
        fields = ['email', 'mobile_number', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        email = attrs.get('email', '').strip() if attrs.get('email') else ''
        mobile = attrs.get('mobile_number', '').strip() if attrs.get('mobile_number') else ''

        if not email and not mobile:
            raise serializers.ValidationError("Either email or mobile number is required.")

        if email and mobile:
            raise serializers.ValidationError("Either email or mobile number is required, not both.")
        
        if email:
            if not re.match(EMAIL_REGEX, email):
                raise serializers.ValidationError("Invalid email address.")

        if mobile:
            if not re.match(MOBILE_REGEX, mobile):
                raise serializers.ValidationError("Invalid mobile number.")

        return attrs


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)

    # make these mutualy exclusive - user either provides email or phone number
    email = serializers.EmailField(required=False, allow_blank=True)
    mobile_number = serializers.CharField(required=False, allow_blank=True)

    
    class Meta:
        model = User
        fields = ['email', 'password', 'password2', 'phone', 'mobile_number', 'role']
        extra_kwargs = {
            'role': {'required': True},
        }


    def validate(self, attrs):
        # password matching validation
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError({"password2": "Passwords don't match."})
        
        email = attrs.get('email', '').strip() if attrs.get('email') else ''
        mobile = attrs.get('mobile_number', '').strip() if attrs.get('mobile_number') else ''

        if not email and not mobile:
            raise serializers.ValidationError("Either email or mobile number is required.")

        if email and mobile:
            raise serializers.ValidationError("Either email or mobile number is required, not both.")
        
        # validate email
        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "A user with this email already exists."})

        # validate mobile number
        if mobile and User.objects.filter(mobile_number=mobile).exists():
            raise serializers.ValidationError({"mobile_number": "A user with this mobile number already exists."})

        if mobile:
            if not re.match(r'^[0-9]{10}$', mobile):
                raise serializers.ValidationError({"mobile_number": "Invalid mobile number."})
        
        return attrs

    
    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password2', None)  # Remove password2 as it's not a model field

        # If email is not provided, generate one from mobile_number
        # Since email is required (USERNAME_FIELD), we need to provide a unique email
        if not validated_data.get('email') or not validated_data.get('email').strip():
            mobile = validated_data.get('mobile_number', '').strip()
            if mobile:
                # Generate a unique email from mobile number
                base_email = f"{mobile}@companio.local"
                email = base_email
                counter = 1
                while User.objects.filter(email=email).exists():
                    email = f"{mobile}+{counter}@companio.local"
                    counter += 1
                validated_data['email'] = email
            else:
                raise serializers.ValidationError("Either email or mobile_number must be provided.")

        user = User.objects.create_user(password=password, **validated_data)
        return user

