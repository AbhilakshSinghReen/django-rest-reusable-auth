from datetime import datetime

from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError

from backend_app.settings import USER_INVITE_JWT_EXPIRY_TIMEDELTA
from core.models.models import CustomUser, UserInvite


class UserInviteCreationForm(forms.ModelForm):
    class Meta:
        model = UserInvite
        fields = ['email', 'name', 'senders_name']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("A user with this email has already been registered.")
        return email


class UserInviteChangeForm(forms.ModelForm):
    class Meta:
        model = UserInvite
        fields = ('email', 'name', 'senders_name', 'invite_sent_at', 'status', 'resend_invite')
        readonly_fields = ('email', 'invite_sent_at', 'status')


class UserInviteAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        if obj:
            self.form = UserInviteChangeForm
        else:
            self.form = UserInviteCreationForm
        
        return super().get_form(request, obj, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['email', 'invite_sent_at', 'status']
        return []

    def save_model(self, request, obj, form, change):
        if not change:
            obj.status = UserInvite.QUEUED
        
        obj.invite_expiry_timestamp=datetime.now() + USER_INVITE_JWT_EXPIRY_TIMEDELTA
        
        super().save_model(request, obj, form, change)
