from datetime import datetime

from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from backend_app.settings import (
    APP_NAME,
    USER_INVITE_JWT_EXPIRY_TIMEDELTA,
    USER_SELF_REGISTRATION_ENABLED,
)
from core.models import CustomUser, UserInvite
from core.serializers import (
    GetUserDataFromInviteTokenRequestBodySerializer,
    SendRegisterInviteViaEmailRequestBodySerializer,
    RegisterUserUsingInviteTokenRequestBodySerializer,
)
from core.utils.jwt_utils import (
    generate_jwt,
    verify_jwt,
)


class RequestEmailUserInviteAPIView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]

    def post(self, request):
        if not USER_SELF_REGISTRATION_ENABLED:
            return Response({
                'success': False,
                'error': {
                    'message': "User registration is through invitation only.",
                    'user_friendly_message': "User registration is through invitation only.",
                },
            }, status=status.HTTP_400_BAD_REQUEST)
        
        body_serializer = SendRegisterInviteViaEmailRequestBodySerializer(data=request.data)
        if not body_serializer.is_valid():
            return Response({
                'success': False,
                'validation_errors': body_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        email = request.data.get('email')
        full_name = request.data.get('name', "None")
        senders_name = "None"

        try:
            existing_user_invite = UserInvite.objects.get(email=email)
            if existing_user_invite.invite_expiry_timestamp > (datetime.now() + USER_INVITE_JWT_EXPIRY_TIMEDELTA):
                user_invite = existing_user_invite
                user_invite.invite_expiry_timestamp = datetime.now() + USER_INVITE_JWT_EXPIRY_TIMEDELTA
                user_invite.save()
        except:
            user_invite = UserInvite.objects.create(
                email=email,
                name=full_name,
                senders_name=senders_name,
                invite_expiry_timestamp=datetime.now() + USER_INVITE_JWT_EXPIRY_TIMEDELTA,
            )
            user_invite.save()
        
        return Response({
            'success': True,
            'result': {
                'user_friendly_message': "Please check your email for steps to continue the registration.",
                'user_invite': {
                    'id': user_invite.id,
                },
            },
        }, status=status.HTTP_201_CREATED)


class GetUserDataFromInviteTokenAPIView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]

    def post(self, request):
        body_serializer = GetUserDataFromInviteTokenRequestBodySerializer(data=request.data)
        if not body_serializer.is_valid():
            return Response({
                'success': False,
                'validation_errors': body_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        token_str = request.data.get('token')

        verification_success, verification_result = verify_jwt(token_str)
        if not verification_success:
            if verification_result == "expired":
                return Response({
                    'success': True,
                    'error': {
                        'message': "Verification token expired.",
                        'user_friendly_message': "The verification link has expired.",
                    },
                }, status=status.HTTP_400_BAD_REQUEST)
            elif verification_result == "invalid":
                return Response({
                    'success': True,
                    'error': {
                        'message': "Verification token invalid.",
                        'user_friendly_message': "The verification link is invalid.",
                    },
                }, status=status.HTTP_400_BAD_REQUEST)
        
        jwt_payload = verification_result
        
        return Response({
            'success': True,
            'result': {
                'user_invite': {
                    'email': jwt_payload['email'],
                    'full_name': jwt_payload['full_name'],
                },
            },
        }, status=status.HTTP_201_CREATED)


class RegisterUserUsingInviteTokenAPIView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]

    def post(self, request):
        body_serializer = RegisterUserUsingInviteTokenRequestBodySerializer(data=request.data)
        if not body_serializer.is_valid():
            return Response({
                'success': False,
                'validation_errors': body_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        token_str = request.data.get('token')
        email = request.data.get('email')
        full_name = request.data.get('full_name')
        password = request.data.get('password')
        
        # Validate token
        verification_success, verification_result = verify_jwt(token_str)
        if not verification_success:
            if verification_result == "expired":
                return Response({
                    'success': False,
                    'error': {
                        'message': "Verification token expired.",
                        'user_friendly_message': "The verification link has expired.",
                    },
                }, status=status.HTTP_400_BAD_REQUEST)
            elif verification_result == "invalid":
                return Response({
                    'success': False,
                    'error': {
                        'message': "Verification token invalid.",
                        'user_friendly_message': "The verification link is invalid.",
                    },
                }, status=status.HTTP_400_BAD_REQUEST)
        
        _jwt_payload = verification_result

        # Find UserInvite object with that token
        try:
            user_invite = UserInvite.objects.get(token=token_str)
        except:
            return Response({
                'success': False,
                'error': {
                    'message': "Verification token invalid.",
                    'user_friendly_message': "The verification link is invalid.",
                },
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Cross check provided email with email of user invite object
        if user_invite.email != email:
            return Response({
                'success': False,
                'error': {
                    'message': "Email provided does not match with the email in the invite.",
                },
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create User and delete the UserInvite object
        user = CustomUser.objects.create(
            email=email,
            full_name=full_name,
            password=password
        )
        user_invite.delete()

        return Response({
            'success': True,
            'result': {
                'message': "User created successfully.",
                'user_friendly_message': "Signup successful.",
                'user': {
                    'id': user.id,
                },
            },
        }, status=status.HTTP_201_CREATED)


# class RegisterUser
# Verify Token, create user, delete invite

# request reset password via email

# verify reset password token

# reset password

# login

# refresh access token

# blacklist refresh token

# sample protected route
