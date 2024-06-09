from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.state import token_backend
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser


class EmailRequestBodySerializer(serializers.Serializer):
    email = serializers.EmailField()


class GetUserDataFromTokenRequestBodySerializer(serializers.Serializer):
    token = serializers.CharField()


class MarkEmailAsSentRequestBodySerializer(serializers.Serializer):
    email_type = serializers.CharField()
    email = serializers.EmailField()


class RegisterUserUsingInviteTokenRequestBodySerializer(serializers.Serializer):
    token = serializers.CharField()
    email = serializers.EmailField()
    full_name = serializers.CharField()
    password = serializers.CharField()


class ResetPasswordUsingResetPasswordTokenRequestBodySerializer(serializers.Serializer):
    token = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        email = attrs['email']
        password = attrs['password']
        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid login credentials.")

        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['user'] = {
            'id': user.id,
            'email':user.email,
            'fullName':user.full_name,
        }

        return token


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        refresh_token_str = attrs['refresh']
        refresh_token = RefreshToken(refresh_token_str)
        decoded_payload = token_backend.decode(refresh_token_str, verify=True)
        user_id = decoded_payload['user_id']

        try:
            user = CustomUser.objects.get(id=user_id)
        except Exception as e:
            print(e)
            raise serializers.ValidationError('Invalid refresh token')
        
        access_token = refresh_token.access_token

        access_token['user'] = {
            'id': user.id,
            'email': user.email,
            'fullName': user.full_name,
        }

        data['access'] = str(access_token)

        return data


class LogoutRequestBodySerializer(serializers.Serializer):
    refresh = serializers.CharField()
