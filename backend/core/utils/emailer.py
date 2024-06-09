from django.db.models import Q

from backend_app.settings import (
    APP_NAME,
    FRONTEND_BASE_URL,
    PASSWORD_RESET_JWT_EXPIRY_TIMEDELTA,
    PASSWORD_RESET_JWT_EXPIRY_TIMEDELTA_IN_WORDS,
    USER_INVITE_JWT_EXPIRY_TIMEDELTA,
    USER_INVITE_JWT_EXPIRY_TIMEDELTA_IN_WORDS,
)
from core.models import CustomUser, UserInvite
from core.redis_client import get_password_reset_via_email_requests
from core.utils.jwt_utils import generate_jwt
from core.utils.templates import load_templates


templates = load_templates()


def generate_user_invite_email_content(content_type, invite):
    invite_token = invite.token
    receivers_name = invite.name
    senders_name = invite.senders_name

    selected_template = "emails/user-invites/complete" + f".{content_type}"

    if senders_name == "None" and receivers_name == "None":
        selected_template = "emails/user-invites/no_sender_no_receiver" + f".{content_type}"
    elif senders_name == "None":
        selected_template = "emails/user-invites/no_sender" + f".{content_type}"
    elif receivers_name == "None":
        selected_template = "emails/user-invites/no_receiver" + f".{content_type}"
    
    populated_template = templates[selected_template]

    registration_url = FRONTEND_BASE_URL + "/auth/complete-signup/" + invite_token

    populated_template = populated_template.replace("{{app_name}}", APP_NAME)
    populated_template = populated_template.replace("{{registration_url}}", registration_url)
    populated_template = populated_template.replace("{{senders_name}}", senders_name)
    populated_template = populated_template.replace("{{receivers_name}}", receivers_name)
    populated_template = populated_template.replace("{{link_expiry_in}}", USER_INVITE_JWT_EXPIRY_TIMEDELTA_IN_WORDS)

    return populated_template


def get_user_invite_emails():
    queued_invites = UserInvite.objects.filter(Q(status=UserInvite.QUEUED) | Q(resend_invite=True))
    
    user_invite_emails = []
    for invite in queued_invites:
        payload = {
            'type': "user_invite_token",
            'email': invite.email,
            'full_name': invite.name,
            'senders_name': invite.senders_name,
            'user_invite': {
                'id': invite.id,
            },
        }
        token = generate_jwt(payload, USER_INVITE_JWT_EXPIRY_TIMEDELTA)

        invite.token = token
        invite.save()

        user_invite_emails.append({
            'type': 'user_invite',
            'receivers_address': invite.email,
            'subject': f"{APP_NAME} Registration",
            'plain_text_content': generate_user_invite_email_content('txt', invite),
            'html_content': generate_user_invite_email_content('html', invite),
        })

    return user_invite_emails


def generate_password_reset_email_content(content_type, user, token):
    user_full_name = user.full_name

    selected_template = "emails/password-reset/primary" + f".{content_type}"

    populated_template = templates[selected_template]

    password_reset_url = FRONTEND_BASE_URL + "/auth/reset-password/" + token

    populated_template = populated_template.replace("{{app_name}}", APP_NAME)
    populated_template = populated_template.replace("{{password_reset_url}}", password_reset_url)
    populated_template = populated_template.replace("{{user_full_name}}", user_full_name)
    populated_template = populated_template.replace("{{link_expiry_in}}", PASSWORD_RESET_JWT_EXPIRY_TIMEDELTA_IN_WORDS)

    return populated_template


def get_password_reset_emails():
    reset_password_requests = get_password_reset_via_email_requests()

    reset_password_emails = []
    for reset_password_request_email_address in reset_password_requests:
        try:
            user = CustomUser.objects.get(email=reset_password_request_email_address)
        except:
            # User does not exist
            continue
        
        payload = {
            'type': "password_reset_token",
            'email': user.email,
            'full_name': user.full_name,
        }
        token = generate_jwt(payload, PASSWORD_RESET_JWT_EXPIRY_TIMEDELTA)

        reset_password_emails.append({
            'type': 'user_password_reset',
            'receivers_address': user.email,
            'subject': f"Reset Your {APP_NAME} Password",
            'plain_text_content': generate_password_reset_email_content('txt', user, token),
            'html_content': generate_password_reset_email_content('html', user, token),
        })
    
    return reset_password_emails
