from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from backend_app.settings import EMAIL_SERVICE_API_KEY
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
        return Response({
            'success': True,
            'result': {
                'message': "Registration successful."
            },
        }, status=status.HTTP_201_CREATED)
    