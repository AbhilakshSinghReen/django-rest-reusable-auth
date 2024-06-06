from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import UserInvite, CustomUser


class SendRegisterInviteViaEmailRequestBodySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInvite
        fields = ['email']


class GetUserDataFromInviteTokenRequestBodySerializer(serializers.Serializer):
    token = serializers.CharField()
