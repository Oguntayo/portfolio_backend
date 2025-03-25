from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from api.utils.response.response import success, error
from .serializers import UserSerializer, LoginSerializer,LogoutSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from api.utils.response.response import success, error
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from api.utils.response.response import success, error
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.response import Response
from api.utils.response.response import success, error
from .models import Profile
from .serializers import ProfileSerializer
from drf_yasg.utils import swagger_auto_schema
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()

class RegisterView(generics.CreateAPIView):
    """User Registration API that returns access & refresh tokens"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.save()
            return success("User registered successfully", data=user_data, status_code=status.HTTP_201_CREATED)
        return error("Registration failed", errors=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    """User Login API - Returns JWT Token"""

    @swagger_auto_schema(
        operation_description="Authenticate user and return JWT tokens",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["email", "password"],
            properties={
                "email": openapi.Schema(type=openapi.TYPE_STRING, format="email", description="User's email"),
                "password": openapi.Schema(type=openapi.TYPE_STRING, description="User's password"),
            },
        ),
        responses={
            200: openapi.Response(
                description="Successful login",
                examples={
                    "application/json": {
                        "status": "success",
                        "status_code": 200,
                        "message": "Login successful",
                        "data": {
                            "access": "eyJhbGciOiJIUzI1...",
                            "refresh": "eyJhbGciOiJIUzI1..."
                        }
                    }
                },
            ),
            400: openapi.Response(
                description="Invalid credentials",
                examples={
                    "application/json": {
                        "status": "error",
                        "status_code": 400,
                        "message": "Login failed",
                        "data": {"error": "Invalid email or password"}
                    }
                },
            ),
        }
    )
    def post(self, request):
        """Login and return JWT tokens"""
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            return success("Login successful", data=serializer.validated_data["tokens"], status_code=200)
        
        return error("Login failed", errors={"error": "Invalid email or password"}, status_code=400)


class LogoutView(APIView):
    """Logout API - Blacklists Refresh Token"""
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Logout user by blacklisting their refresh token",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["refresh"],
            properties={
                "refresh": openapi.Schema(type=openapi.TYPE_STRING, description="Refresh token to be blacklisted"),
            },
        ),
        responses={
            200: openapi.Response(
                description="Successfully logged out",
                examples={
                    "application/json": {
                        "status": "success",
                        "status_code": 200,
                        "message": "Logout successful",
                        "data": {}
                    }
                },
            ),
            400: openapi.Response(description="Invalid refresh token"),
            401: openapi.Response(description="User is not authenticated"),
        }
    )
    def post(self, request):
        """Automatically extract and blacklist the refresh token"""
        refresh_token = request.data.get("refresh")  # Get refresh token from request body

        if not refresh_token:
            return error("No refresh token provided", errors={"error": "Refresh token is required"}, status_code=400)

        try:
            token = RefreshToken(refresh_token)  # Convert string to RefreshToken object
            token.blacklist()  # Blacklist the refresh token
            
            return success("Logout successful", data={}, status_code=200)

        except Exception:
            return error("Invalid token", errors={"error": "Token is not refreshable"}, status_code=400)

class ProfileView(generics.RetrieveUpdateAPIView):
    """Retrieve & Update Profile"""
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Ensure user can only access their own profile"""
        return self.request.user.profile

    @swagger_auto_schema(
        operation_description="Retrieve the authenticated user's profile.",
        responses={200: ProfileSerializer()},
    )
    def get(self, request, *args, **kwargs):
        """Get user profile"""
        return success("Profile retrieved successfully", data=self.get_serializer(self.get_object()).data)

    @swagger_auto_schema(
        operation_description="Update the authenticated user's profile.",
        request_body=ProfileSerializer,
        responses={200: ProfileSerializer()},
    )
    def put(self, request, *args, **kwargs):
        """Update user profile"""
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success("Profile updated successfully", data=serializer.data)
        return error("Profile update failed", errors=serializer.errors)



class GoogleLoginView(SocialLoginView):
    """Google OAuth Login API - Returns JWT Tokens"""
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    callback_url = settings.SOCIAL_AUTH_GOOGLE_REDIRECT_URI  

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)  
        user = self.user 

        if user: 
            refresh = RefreshToken.for_user(user) 
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            return Response({
                "access": access_token,
                "refresh": refresh_token,
                "email": user.email,
                "username": user.username
            })
        return response  
