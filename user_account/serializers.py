from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile
from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomRegisterSerializer(RegisterSerializer):
    username = None 

    def get_cleaned_data(self):
        return {
            "email": self.validated_data.get("email", ""),
            "password1": self.validated_data.get("password1", ""),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        user.save()
        return user



class UserSerializer(serializers.ModelSerializer):
    """Serializer for user registration that returns JWT tokens"""
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'access', 'refresh']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """Create user & generate tokens"""
        user = User.objects.create_user(**validated_data)  
        refresh = RefreshToken.for_user(user)  
        return {
            "id": user.id,
            "email": user.email,
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }
class LoginSerializer(serializers.Serializer):
    """Serializer for user login with JWT tokens"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """Authenticate user and return JWT tokens"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(email=email, password=password)  # Authenticate with email
        if not user:
            raise serializers.ValidationError("Invalid email or password")

        return {
            "user": user,
            "tokens": self.get_tokens(user)
        }

    def get_tokens(self, user):
        """Generate JWT tokens"""
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        
class LogoutSerializer(serializers.Serializer):
    """Serializer for logging out and blacklisting refresh token"""
    refresh = serializers.CharField()

    def validate(self, data):
        """Blacklist the refresh token"""
        try:
            refresh_token = RefreshToken(data["refresh"])
            refresh_token.blacklist()  # Blacklist token so it can't be used again
        except Exception as e:
            raise serializers.ValidationError("Invalid refresh token")

        return data

class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile"""
    email = serializers.ReadOnlyField(source="user.email")  # Show email but make it read-only
    profile_picture = serializers.ImageField(required=False)  # Allow image upload

    class Meta:
        model = Profile
        fields = ["email", "bio", "profile_picture", "website", "twitter"]

    def update(self, instance, validated_data):
        """Handle updating the profile"""
        instance.bio = validated_data.get("bio", instance.bio)
        instance.website = validated_data.get("website", instance.website)
        instance.twitter = validated_data.get("twitter", instance.twitter)

        # Only update profile picture if provided
        if "profile_picture" in validated_data:
            instance.profile_picture = validated_data["profile_picture"]

        instance.save()
        return instance
