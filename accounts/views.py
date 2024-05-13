from django.shortcuts import render
from rest_framework.views import APIView
from .api.serializers import LoginSerializer,UserRegistrationSerializer
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .models import User
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.permissions import AllowAny




#  Login api
class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            user = authenticate(request, email=email, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    }
                )
            else:
                # Authentication failed
                return Response(
                    {"message": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        else:
            # Invalid data
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
               
# Register api
class UserRegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            # Check if user exits
            phone_number = serializer.validated_data["phone_number"]
            if User.objects.filter(phone_number=phone_number).exists():
                return Response(
                    {
                        "error": "User with the provided username or email already exists"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Get access token api
class TokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]
