from django.contrib import admin

from core.models import UserInvite


def send_invite():
    print("foo")


class UserInviteAdmin(admin.ModelAdmin):
    model = UserInvite

    list_display = ('email', 'name', 'senders_name')
    search_fields = ('email', 'name', 'senders_name')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['email', 'invite_sent_at']
        return ['invite_sent_at']
