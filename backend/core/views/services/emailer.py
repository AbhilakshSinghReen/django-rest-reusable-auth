from datetime import datetime

from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from backend_app.settings import EMAIL_SERVICE_API_KEY
from core.models import UserInvite
from core.redis_client import remove_password_reset_via_email_request
from core.serializers import MarkEmailAsSentRequestBodySerializer
from core.utils.emailer import (
    get_user_invite_emails,
    get_password_reset_emails,
)


class GetEmailsToSendAPIView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]

    def get(self, request):
        api_key = request.headers.get('X-SERVICE-API-KEY')

        if api_key != EMAIL_SERVICE_API_KEY:
            return Response({
                'success': False,
                'error': {
                    'message': "Invalid API key",
                },
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response({
            'success': True,
            'result': {
                'emails': get_user_invite_emails() + get_password_reset_emails(),
            },
        }, status=status.HTTP_201_CREATED)


class MarkEmailAsSentAPIView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]

    def post(self, request):
        api_key = request.headers.get('X-SERVICE-API-KEY')

        if api_key != EMAIL_SERVICE_API_KEY:
            return Response({
                'success': False,
                'error': {
                    'message': "Invalid API key",
                },
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        body_serializer = MarkEmailAsSentRequestBodySerializer(data=request.data)
        if not body_serializer.is_valid():
            return Response({
                'success': False,
                'validation_errors': body_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        email_type = request.data.get('email_type')
        email = request.data.get('email')

        if email_type == "user_invite":
            try:
                user_invite = UserInvite.objects.get(email=email)
                user_invite.status = UserInvite.SENT
                user_invite.invite_sent_at = datetime.now()
                user_invite.resend_invite = False
                user_invite.save()
            except:
                pass
        elif email_type == "user_password_reset":
            remove_password_reset_via_email_request(email)
        else:
            return Response({
                'success': False,
                'error': {
                    'message': "Invalid email type.",
                },
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'success': True,
            'result': {
                'message': "Email has been marked as sent."
            },
        }, status=status.HTTP_200_OK)
    