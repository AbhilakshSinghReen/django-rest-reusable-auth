from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class GetUserInvitesAPIView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]

    def post(self, request):
        return Response({
            'success': True,
            'result': {
                'message': "Registration successful."
            },
        }, status=status.HTTP_201_CREATED)


class MarkInviteEmailsAsSentAPIView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]

    def post(self, request):
        return Response({
            'success': True,
            'result': {
                'message': "Registration successful."
            },
        }, status=status.HTTP_201_CREATED)
    