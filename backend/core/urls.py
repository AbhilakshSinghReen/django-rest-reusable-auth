from django.urls import path

from core.views.auth import (
    RequestEmailUserInviteAPIView,
    GetUserDataFromInviteTokenAPIView,
)
from core.views.services.email_views import (
    GetUserInvitesAPIView,
    MarkInviteEmailsAsSentAPIView,
)


urlpatterns = [
    path('auth/request-email-user-invite/', RequestEmailUserInviteAPIView.as_view(), name='auth_register'),
    path('auth/get-user-data-from-invite-token/', GetUserDataFromInviteTokenAPIView.as_view(), name='auth_register1'),

    path('services/email/get-user-invites/', GetUserInvitesAPIView.as_view(), name='get_user_invites'),
    path('services/email/mark-invite-emails-as-sent/', MarkInviteEmailsAsSentAPIView.as_view(), name='mark_invite_emails_as_sent'),
]
