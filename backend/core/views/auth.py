from datetime import datetime

from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from backend_app.settings import (
    USER_INVITE_JWT_EXPIRY_TIMEDELTA,
    USER_SELF_REGISTRATION_ENABLED,
)
from core.models import CustomUser, UserInvite
from core.redis_client import (
    add_password_reset_via_email_request,
)
from core.serializers import (
    GetUserDataFromTokenRequestBodySerializer,
    EmailRequestBodySerializer,
    RegisterUserUsingInviteTokenRequestBodySerializer,
    CustomTokenObtainPairSerializer,
    CustomTokenRefreshSerializer,
    LogoutRequestBodySerializer,
    ResetPasswordUsingResetPasswordTokenRequestBodySerializer,
)
from core.utils.jwt_utils import (
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
        
        body_serializer = EmailRequestBodySerializer(data=request.data)
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
            try:
                user_invite = UserInvite.objects.create(
                    email=email,
                    name=full_name,
                    senders_name=senders_name,
                    invite_expiry_timestamp=datetime.now() + USER_INVITE_JWT_EXPIRY_TIMEDELTA,
                )
                user_invite.save()
            except ValidationError as validation_error:
                return Response({
                    'success': False,
                    'error': {
                        'user_friendly_message': validation_error,
                    },
                }, status=status.HTTP_201_CREATED)
        
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
        body_serializer = GetUserDataFromTokenRequestBodySerializer(data=request.data)
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
        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            full_name=full_name
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


class RequestPasswordResetViaEmailAPIView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]

    def post(self, request):
        body_serializer = EmailRequestBodySerializer(data=request.data)
        if not body_serializer.is_valid():
            return Response({
                'success': False,
                'validation_errors': body_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        email = request.data.get('email')

        add_password_reset_via_email_request(email)

        return Response({
            'success': True,
            'result': {
                'user_friendly_message': "Please check your email to reset your password.",
            },
        }, status=status.HTTP_200_OK)


class GetUserDataFromPasswordResetTokenAPIView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]

    def post(self, request):
        body_serializer = GetUserDataFromTokenRequestBodySerializer(data=request.data)
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
                'user': {
                    'email': jwt_payload['email'],
                    'full_name': jwt_payload['full_name'],
                },
            },
        }, status=status.HTTP_201_CREATED)


class ResetPasswordUsingPasswordResetTokenAPIView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]

    def post(self, request):
        body_serializer = ResetPasswordUsingResetPasswordTokenRequestBodySerializer(data=request.data)
        if not body_serializer.is_valid():
            return Response({
                'success': False,
                'validation_errors': body_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        token_str = request.data.get('token')
        email = request.data.get('email')
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
        
        jwt_payload = verification_result

        # Cross check provided email with email of user invite object
        if jwt_payload['email'] != email:
            return Response({
                'success': False,
                'error': {
                    'message': "Email provided does not match with the email corresponding to the link.",
                },
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Find User object with that email and update its password
        try:
            user = CustomUser.objects.get(email=email)
            user.set_password(password)
            user_invite = UserInvite.objects.get(token=token_str)
        except:
            return Response({
                'success': False,
                'error': {
                    'message': "Verification token invalid.",
                    'user_friendly_message': "The verification link is invalid.",
                },
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'success': True,
            'result': {
                'message': "Password reset successful.",
                'user_friendly_message': "Password reset successful.",
                'user': {
                    'id': user.id,
                },
            },
        }, status=status.HTTP_200_OK)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer


class LogoutAPIView(APIView):
    def post(self, request):
        body_serializer = LogoutRequestBodySerializer(data=request.data)
        if not body_serializer.is_valid():
            return Response({
                'success': False,
                'validation_errors': body_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        token = RefreshToken(request.data.get('refresh'))
        token.blacklist()

        return Response({
            'success': True,
            'result': {
                'message': "Logout successful.",
                'user_friendly_message': "Logout successful.",
            }
        }, status=status.HTTP_200_OK)


class GetFooAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, _request):
        return Response({
            'success': True,
            'result': {
                'message': "foo",
                'user_friendly_message': "foo",
            },
        }, status=status.HTTP_200_OK)
