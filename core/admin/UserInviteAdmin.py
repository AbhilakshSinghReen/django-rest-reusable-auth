from django.contrib import admin
from django.utils import timezone


from core.models.models import UserInvite
from django import forms



def send_invite():
    print("foo")


class UserInviteCreationForm(forms.ModelForm):
    class Meta:
        model = UserInvite
        fields = ['email', 'name', 'senders_name']


class UserInviteAdmin(admin.ModelAdmin):
    form = UserInviteCreationForm

    def save_model(self, request, obj, form, change):
        if not change:  # If this is a new object
            obj.invite_sent_at = timezone.now()
            obj.status = UserInvite.QUEUED
        super().save_model(request, obj, form, change)

