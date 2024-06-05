from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from backend_app.settings import APP_NAME
from core.models import UserInvite
from core.serializers import (
    GetUserDataFromInviteTokenRequestBodySerializer,
    SendRegisterInviteViaEmailRequestBodySerializer,
)


class RequestEmailUserInviteAPIView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]

    def post(self, request):
        body_serializer = SendRegisterInviteViaEmailRequestBodySerializer(data=request.data)
        if not body_serializer.is_valid():
            return Response({
                'success': False,
                'errors': body_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        email = request.data.get('email')
        full_name = request.data.get('name')
        senders_name = f"{APP_NAME} Auth Service"

        try:
            user_invite = UserInvite.objects.create(
                email=email,
                name=full_name,
                senders_name=senders_name
            )
            user_invite.save()
        except ValidationError as e:
            return Response({
                'success': False,
                'error': {
                    'message': str(e),
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        
        payload = {
            'email': email,
            'full_name': full_name,
            'senders_name': senders_name,
            'user_invite': {
                'id': user_invite.id,
            },
        }
        
        token = AccessToken()
        token.payload = payload
        print(str(token))
        
        return Response({
            'success': True,
            'result': {
                'user_invite': {
                    'id': user_invite.id,
                },
            },
        }, status=status.HTTP_201_CREATED)


class GetUserDataFromInviteTokenAPIView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]

    def get(self, request):
        body_serializer = GetUserDataFromInviteTokenRequestBodySerializer(data=request.data)
        if not body_serializer.is_valid():
            return Response({
                'success': False,
                'errors': body_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        token = request.data.get('token')



        # full_name = request.data.get('name')

        # try:
        #     user_invite = UserInvite.objects.create(
        #         email=email,
        #         name=full_name,
        #         senders_name=f"{APP_NAME} Auth Service"
        #     )
        #     user_invite.save()
        # except ValidationError as e:
        #     return Response({
        #         'success': False,
        #         'error': {
        #             'message': str(e),
        #         }
        #     }, status=status.HTTP_400_BAD_REQUEST)
        
        # return Response({
        #     'success': True,
        #     'result': {
        #         'user_invite': {
        #             'id': user_invite.id,
        #         },
        #     },
        # }, status=status.HTTP_201_CREATED)