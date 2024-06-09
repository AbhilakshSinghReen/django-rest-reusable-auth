from django.urls import path


from core.views.auth import (
    RequestEmailUserInviteAPIView,
    GetUserDataFromInviteTokenAPIView,
    RegisterUserUsingInviteTokenAPIView,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    LogoutAPIView,
)
from core.views.services.emailer import (
    GetEmailsToSendAPIView,
    MarkEmailAsSentAPIView,
)


urlpatterns = [
    path('auth/request-email-user-invite/', RequestEmailUserInviteAPIView.as_view(), name='request_email_user_invite'),
    path('auth/get-user-data-from-invite-token/', GetUserDataFromInviteTokenAPIView.as_view(), name='get_user_data_from_invite_token'),
    path('auth/signup-using-invite-token/', RegisterUserUsingInviteTokenAPIView.as_view(), name='signup_using_invite_token'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('auth/token/refresh/', CustomTokenRefreshView.as_view(), name="token_refresh"),
    path('auth/logout/', LogoutAPIView.as_view(), name="logout"),

    path('services/emailer/get-emails-to-send/', GetEmailsToSendAPIView.as_view(), name='get_emails_to_send'),
    path('services/emailer/mark-email-as-sent/', MarkEmailAsSentAPIView.as_view(), name='mark_email_as_sent'),
]
