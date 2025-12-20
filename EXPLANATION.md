# Line-by-Line Explanation: Models & Serializers

## How Serializers Link to Views

**NOT indexing!** Serializers are linked through **class attributes** and **method calls**:

```python
# In views.py
class UserRegisterView(GenericAPIView):
    serializer_class = UserRegistrationSerializer  # ← Direct class reference
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)  # DRF gets the linked serializer
        serializer.save()  # Calls serializer.create() which creates User model
```

---

## 📋 MODELS.PY - Line by Line

### Line 1: `from django.db import models`
- **What**: Imports Django's model base classes and field types
- **Why**: Needed to define database tables as Python classes
- **Function**: Provides `models.Model`, `models.CharField`, etc.

### Line 2: `from django.contrib.auth.models import AbstractUser`
- **What**: Imports Django's built-in user model template
- **Why**: We extend it instead of creating from scratch
- **Function**: Gives us username, password, email, is_active, etc. for free

### Line 4: `class User(AbstractUser):`
- **What**: Defines our custom User model, inheriting from AbstractUser
- **Why**: We need to add custom fields (phone, role) while keeping Django auth features
- **Function**: Creates a database table called `users_user` with all AbstractUser fields + our custom ones

### Lines 6-9: `ROLE_CHOICES = (...)`
- **What**: Tuple of tuples defining valid role options
- **Why**: Restricts role field to only 'BOOKER' or 'COMPANION'
- **Function**: Used by Django admin and forms to show dropdown options
- **Format**: `('DB_VALUE', 'Human Readable Label')`

### Line 11: `phone = models.CharField(max_length=20, unique=True, blank=True, null=True)`
- **What**: Phone number field
- **Why**: Users might not have phone initially
- **Parameters**:
  - `max_length=20`: Max 20 characters
  - `unique=True`: No two users can have same phone
  - `blank=True`: Form can be submitted empty
  - `null=True`: Database can store NULL value
- **Function**: Creates VARCHAR(20) column in database

### Line 12: `email = models.EmailField(unique=True)`
- **What**: Email field with validation
- **Why**: Email is USERNAME_FIELD (line 16), must be unique
- **Function**: Validates email format + creates unique constraint in database

### Line 13: `role = models.CharField(max_length=20, choices=ROLE_CHOICES)`
- **What**: Role field restricted to choices
- **Why**: Only BOOKER or COMPANION allowed
- **Function**: Creates VARCHAR(20) with CHECK constraint in database

### Line 14: `date_joined = models.DateTimeField(auto_now_add=True)`
- **What**: Timestamp when user registered
- **Why**: Track when account was created
- **Function**: Automatically sets to current time when User is first saved
- **Note**: `auto_now_add` = set once, `auto_now` = update every save

### Line 16: `USERNAME_FIELD = 'email'`
- **What**: Tells Django to use email for login instead of username
- **Why**: Users login with email, not username
- **Function**: Changes authentication behavior - `authenticate(email=..., password=...)`

### Line 17: `REQUIRED_FIELDS = ['role']`
- **What**: Fields required when creating superuser via `createsuperuser`
- **Why**: Email is USERNAME_FIELD, so can't be in REQUIRED_FIELDS
- **Function**: Django CLI will prompt for 'role' when creating admin user

### Line 19-20: `def __str__(self):`
- **What**: String representation of User object
- **Why**: Shows readable name in Django admin and debug
- **Function**: Returns "john_doe (BOOKER)" instead of "User object (1)"

---

### Line 23: `class Profile(models.Model):`
- **What**: Separate model for user profile information
- **Why**: Keeps User model clean, allows optional profile data
- **Function**: Creates `users_profile` table in database

### Line 24: `user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')`
- **What**: One-to-one relationship with User
- **Why**: Each user has exactly one profile, each profile belongs to one user
- **Parameters**:
  - `on_delete=models.CASCADE`: If User deleted, Profile is deleted too
  - `related_name='profile'`: Access profile via `user.profile` (not `user.profile_set`)
- **Function**: Creates foreign key + unique constraint in database

### Line 25: `bio = models.TextField(blank=True, null=True)`
- **What**: Biography text field (unlimited length)
- **Why**: Users can write long bios
- **Function**: Creates TEXT column in database

### Line 26: `avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)`
- **What**: Image upload field
- **Why**: Users can upload profile pictures
- **Function**: Creates VARCHAR(100) storing file path, files saved to `media/avatars/`

### Line 27: `updated_at = models.DateTimeField(auto_now=True)`
- **What**: Timestamp of last profile update
- **Why**: Track when profile was last modified
- **Function**: Automatically updates to current time every time Profile is saved

### Line 28: `address = models.CharField(max_length=255, blank=True, null=True)`
- **What**: Address field
- **Why**: Optional location information
- **Function**: Creates VARCHAR(255) column

### Line 30-31: `def __str__(self):`
- **What**: String representation of Profile
- **Function**: Returns "Profile of john_doe"

---

## 📝 SERIALIZER.PY - Line by Line

### Line 1: `from rest_framework import serializers`
- **What**: Imports DRF serializer base classes
- **Why**: Need `ModelSerializer` to convert models to/from JSON
- **Function**: Provides serialization framework

### Line 2: `from django.contrib.auth.password_validation import validate_password`
- **What**: Imports Django's password validator
- **Why**: Enforce strong passwords during registration
- **Function**: Checks password strength (length, complexity, etc.)

### Line 3: `from .models import User, Profile`
- **What**: Imports our models
- **Why**: Serializers need to know which models to serialize
- **Function**: Links serializers to database models

---

### Line 6: `class ProfileSerializer(serializers.ModelSerializer):`
- **What**: Serializer for Profile model
- **Why**: Convert Profile objects to JSON and vice versa
- **Function**: Handles Profile data in API requests/responses

### Line 8: `class Meta:`
- **What**: Inner class configuring the serializer
- **Why**: DRF convention for serializer settings
- **Function**: Tells serializer which model and fields to use

### Line 9: `model = Profile`
- **What**: Links serializer to Profile model
- **Why**: Serializer needs to know which database table
- **Function**: Enables automatic field generation from model

### Line 10: `fields = ['id', 'bio', 'avatar', 'address', 'updated_at']`
- **What**: List of fields to include in JSON
- **Why**: Control what data is exposed in API
- **Function**: Only these fields appear in API response

### Line 11: `read_only_fields = ['updated_at']`
- **What**: Fields that can't be set via API
- **Why**: `updated_at` is auto-managed by model
- **Function**: Field appears in GET but ignored in POST/PUT

---

### Line 14: `class UserSerializer(serializers.ModelSerializer):`
- **What**: Basic user serializer for lists
- **Why**: Lightweight version without nested profile
- **Function**: Fast serialization for user lists

### Line 18: `fields = ['id', 'username', 'email', ...]`
- **What**: User fields to expose
- **Why**: Excludes password, nested profile for performance
- **Function**: Returns basic user info in JSON format

### Line 19: `read_only_fields = ['id', 'date_joined']`
- **What**: Fields users can't modify
- **Why**: ID and date_joined are auto-generated
- **Function**: These appear in response but ignored in updates

---

### Line 22: `class UserDetailSerializer(serializers.ModelSerializer):`
- **What**: User serializer with nested profile
- **Why**: When you need full user info including profile
- **Function**: Returns user + profile in one response

### Line 24: `profile = ProfileSerializer(read_only=True)`
- **What**: Nested serializer for profile relationship
- **Why**: Include profile data within user response
- **Function**: Creates nested JSON: `{"user": {...}, "profile": {...}}`
- **read_only=True**: Profile can't be created/updated through this serializer

### Line 28-29: `fields = [..., 'profile']`
- **What**: Includes 'profile' in fields list
- **Why**: ProfileSerializer handles the nested data
- **Function**: Profile data appears nested in response

---

### Line 33: `class UserRegistrationSerializer(serializers.ModelSerializer):`
- **What**: Special serializer for user registration
- **Why**: Needs password handling that other serializers don't
- **Function**: Creates new users with password validation

### Line 35: `password = serializers.CharField(write_only=True, required=True, validators=[validate_password])`
- **What**: Password field definition
- **Why**: Passwords should never appear in API responses
- **Parameters**:
  - `write_only=True`: Appears in POST request, NOT in GET response
  - `required=True`: Must be provided
  - `validators=[validate_password]`: Enforces strong passwords
- **Function**: Accepts password, validates it, but never returns it

### Line 36: `password2 = serializers.CharField(write_only=True, required=True, label='Confirm Password')`
- **What**: Password confirmation field
- **Why**: Users must type password twice to avoid typos
- **Function**: Used only for validation, not stored

### Line 40: `fields = ['username', 'email', 'password', 'password2', ...]`
- **What**: Fields needed for registration
- **Why**: Includes password fields that other serializers exclude
- **Function**: Defines registration form structure

### Line 42-45: `extra_kwargs = {...}`
- **What**: Additional field configuration
- **Why**: Override default field settings
- **Function**: Makes email and role required even if model allows blank

### Line 47: `def validate(self, attrs):`
- **What**: Custom validation method
- **Why**: Check password match (can't do this in field-level validation)
- **Function**: Runs after all field validations, receives all field values
- **attrs**: Dictionary of all validated field values

### Line 48-49: Password matching check
- **What**: Compares password and password2
- **Why**: Ensure user typed password correctly twice
- **Function**: Raises error if passwords don't match

### Line 52: `def create(self, validated_data):`
- **What**: Override default create method
- **Why**: Need to handle password separately (can't store plain text)
- **Function**: Called when `serializer.save()` is executed
- **validated_data**: Dictionary of validated field values

### Line 53: `validated_data.pop('password2')`
- **What**: Remove password2 from data
- **Why**: password2 is only for validation, not stored
- **Function**: Removes confirmation field before creating user

### Line 54: `password = validated_data.pop('password')`
- **What**: Extract password separately
- **Why**: `create_user()` needs password as separate argument
- **Function**: Gets password out of validated_data dict

### Line 55: `user = User.objects.create_user(password=password, **validated_data)`
- **What**: Create user with hashed password
- **Why**: `create_user()` hashes password, regular `create()` doesn't
- **Function**: Creates User in database with properly hashed password
- **`**validated_data`**: Unpacks remaining fields (username, email, etc.)

---

### Line 59: `class UserUpdateSerializer(serializers.ModelSerializer):`
- **What**: Serializer for updating existing users
- **Why**: Different fields than registration (no password)
- **Function**: Handles PATCH/PUT requests for user updates

### Line 63: `fields = ['username', 'email', 'phone', ...]`
- **What**: Only updatable fields
- **Why**: Excludes password, role, id (shouldn't change)
- **Function**: Defines what users can modify

### Line 65: `'email': {'required': False}`
- **What**: Make email optional in updates
- **Why**: Users might only want to update username, not email
- **Function**: Allows partial updates

### Line 68: `def validate_email(self, value):`
- **What**: Field-level validation for email
- **Why**: Check email uniqueness when updating
- **Function**: Runs automatically when email field is validated
- **value**: The email value being validated

### Line 69: `user = self.instance`
- **What**: Get the user being updated
- **Why**: Need to exclude current user from uniqueness check
- **Function**: `self.instance` is the existing User object

### Line 70: `if User.objects.filter(email=value).exclude(pk=user.pk).exists():`
- **What**: Check if another user has this email
- **Why**: Email must be unique, but current user can keep their email
- **Function**: 
  - `filter(email=value)`: Find users with this email
  - `.exclude(pk=user.pk)`: Exclude the current user
  - `.exists()`: Returns True if any other user found

### Line 71: `raise serializers.ValidationError(...)`
- **What**: Raise validation error
- **Why**: Prevent duplicate emails
- **Function**: Returns 400 error with message to client

---

### Line 75: `class ProfileUpdateSerializer(serializers.ModelSerializer):`
- **What**: Serializer for updating profiles
- **Why**: Separate from user updates
- **Function**: Handles profile-specific updates

### Line 79: `fields = ['bio', 'avatar', 'address']`
- **What**: Only updatable profile fields
- **Why**: Excludes id, updated_at (auto-managed)
- **Function**: Defines profile update structure

---

## 🔗 How They Connect

```
HTTP Request → URL → View → Serializer → Model → Database
                ↓
         POST /api/users/register/
                ↓
         UserRegisterView.post()
                ↓
         UserRegistrationSerializer(data=request.data)
                ↓
         serializer.is_valid() → validates data
                ↓
         serializer.save() → calls serializer.create()
                ↓
         User.objects.create_user(...) → creates in database
                ↓
         Response with user data
```

**Key Points:**
- Views link serializers via `serializer_class` attribute
- Serializers link models via `model = ModelName` in Meta class
- Serializers convert between JSON ↔ Python objects ↔ Database rows
- Each serializer has a specific purpose (list, detail, create, update)

