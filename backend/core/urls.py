from django.urls import path

from core.views.auth import (
    RequestEmailUserInviteAPIView,
    GetUserDataFromInviteTokenAPIView,
)
from core.views.services.emailer import (
    GetEmailsToSendAPIView,
    MarkEmailAsSentAPIView,
)


urlpatterns = [
    path('auth/request-email-user-invite/', RequestEmailUserInviteAPIView.as_view(), name='auth_register'),
    path('auth/get-user-data-from-invite-token/', GetUserDataFromInviteTokenAPIView.as_view(), name='auth_register1'),

    path('services/emailer/get-emails-to-send/', GetEmailsToSendAPIView.as_view(), name='get_emails_to_send'),
    path('services/emailer/mark-email-as-sent/', MarkEmailAsSentAPIView.as_view(), name='mark_email_as_sent'),
]
