from django.db.models import Q

from backend_app.settings import APP_NAME, FRONTEND_BASE_URL, USER_INVITE_JWT_EXPIRY_TIMEDELTA
from core.models import UserInvite
from core.redis_client import get_password_reset_via_email_requests
from core.utils.jwt_utils import generate_jwt
from core.utils.templates import load_templates


templates = load_templates()


def generate_user_invite_content(content_type, invite):
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
            'plain_text_content': generate_user_invite_content('txt', invite),
            'html_content': generate_user_invite_content('html', invite),
        })

    return user_invite_emails


def get_password_reset_emails():
    return []
