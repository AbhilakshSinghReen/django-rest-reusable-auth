from django.urls import path


from core.views.auth import (
    RequestEmailUserInviteAPIView,
    GetUserDataFromInviteTokenAPIView,
    RegisterUserUsingInviteTokenAPIView,
    RequestPasswordResetViaEmailAPIView,
    GetUserDataFromPasswordResetTokenAPIView,
    ResetPasswordUsingPasswordResetTokenAPIView,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    LogoutAPIView,
    GetFooAPIView,
)
from core.views.services.emailer import (
    GetEmailsToSendAPIView,
    MarkEmailAsSentAPIView,
)


urlpatterns = [
    # User Invitation and Signup
    path('auth/request-email-user-invite/', RequestEmailUserInviteAPIView.as_view(), name='request_email_user_invite'),
    path('auth/get-user-data-from-invite-token/', GetUserDataFromInviteTokenAPIView.as_view(), name='get_user_data_from_invite_token'),
    path('auth/signup-using-invite-token/', RegisterUserUsingInviteTokenAPIView.as_view(), name='signup_using_invite_token'),
    
    # Password Reset
    path('auth/request-password-reset-via-email/', RequestPasswordResetViaEmailAPIView.as_view(), name='request_password_reset_via_email'),
    path('auth/get-user-data-from-password-reset-token/', GetUserDataFromPasswordResetTokenAPIView.as_view(), name='get_user_data_from_password_reset_token'),
    path('auth/reset-password-using-password-reset-token/', ResetPasswordUsingPasswordResetTokenAPIView.as_view(), name='reset_password_using_password_reset_token'),
    
    # Access and Refresh Tokens
    path('auth/login/', CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('auth/token/refresh/', CustomTokenRefreshView.as_view(), name="token_refresh"),
    path('auth/logout/', LogoutAPIView.as_view(), name="logout"),
    path('auth/get-foo/', GetFooAPIView.as_view(), name="get_foo"),
    
    ### Services
    # Emailer
    path('services/emailer/get-emails-to-send/', GetEmailsToSendAPIView.as_view(), name='get_emails_to_send'),
    path('services/emailer/mark-email-as-sent/', MarkEmailAsSentAPIView.as_view(), name='mark_email_as_sent'),
]
