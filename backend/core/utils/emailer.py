from backend_app.settings import APP_NAME, FRONTEND_BASE_URL
from core.models import UserInvite
from core.redis_client import get_password_reset_via_email_requests
from core.utils.templates import load_templates


templates = load_templates()


def generate_user_invite_plain_text_content(invite_token, receivers_name=None, senders_name=None):
    selected_template = "emails/user-invites/complete.txt"

    if senders_name is None and receivers_name is None:
        selected_template = "emails/user-invites/no_sender_no_receiver.txt"
    elif senders_name is None:
        selected_template = "emails/user-invites/no_sender.txt"
    elif receivers_name is None:
        selected_template = "emails/user-invites/no_receiver.txt"
    
    populated_template = templates[selected_template]

    registration_url = FRONTEND_BASE_URL + "/auth/complete-signup/" + invite_token

    populated_template = populated_template.replace("{{app_name}}", APP_NAME)
    populated_template = populated_template.replace("{{registration_url}}", registration_url)
    populated_template = populated_template.replace("{{senders_name}}", senders_name)
    populated_template = populated_template.replace("{{receivers_name}}", receivers_name)

    return populated_template


def construct_user_invite_email(invite):
    email = {
        'type': 'user_invite',
        'receivers_address': invite.email,
        'subject': f"{APP_NAME} Registration",
        'plain_text_content': "",
        'html_content': "",
    }
    return email


def get_user_invite_emails():
    queued_invites = UserInvite.objects.filter(status=UserInvite.QUEUED)
    user_invite_emails = [construct_user_invite_email(invite) for invite in queued_invites]
    return user_invite_emails


def get_password_reset_emails():
    pass
