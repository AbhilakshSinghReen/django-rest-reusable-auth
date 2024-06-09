from email.message import EmailMessage
import smtplib
from time import sleep
import traceback

from decouple import config
import requests

from admin_emails import construct_warning_email


POLL_PERIOD = config('POLL_PERIOD', cast=int)
SMTP_HOST = config('SMTP_HOST')
EMAIL_SERVICE_API_KEY_HEADER_NAME = config('EMAIL_SERVICE_API_KEY_HEADER_NAME')
EMAIL_SERVICE_API_KEY = config('EMAIL_SERVICE_API_KEY')
GET_EMAILS_TO_SEND_ENDPOINT = config('GET_EMAILS_TO_SEND_ENDPOINT')
MARK_EMAIL_AS_SENT_ENDPOINT = config('MARK_EMAIL_AS_SENT_ENDPOINT')
SENDERS_EMAIL_ADDRESS = config('SENDERS_EMAIL_ADDRESS')
SENDERS_EMAIL_PASSWORD = config('SENDERS_EMAIL_PASSWORD')
ADMIN_EMAIL_FAIL_COUNT_THRESHOLD = config('ADMIN_EMAIL_FAIL_COUNT_THRESHOLD')
ADMIN_EMAIL_ADDRESS = config('ADMIN_EMAIL_ADDRESS')


logger = print


class EmailServiceHandler:
    def __init__(self):
        self.request_headers = {
            EMAIL_SERVICE_API_KEY_HEADER_NAME: EMAIL_SERVICE_API_KEY,
        }

        self.get_consecutive_fail_count = 0
        self.mark_consecutive_fail_count = 0

        self.warning_emails_to_send = []

    def get_emails_to_send(self):
        response = requests.get(GET_EMAILS_TO_SEND_ENDPOINT, headers=self.request_headers)

        if not response.status_code != 200:
            self.get_consecutive_fail_count += 1

            logger(f"Failed to get emails to send from endpoint: {GET_EMAILS_TO_SEND_ENDPOINT}")

            # if self.get_consecutive_fail_count > ADMIN_EMAIL_FAIL_COUNT_THRESHOLD:
            #     self.get_consecutive_fail_count = 0

            #     # self.warning_emails_to_send.a

            #     return [
            #         construct_warning_email(
            #             ADMIN_EMAIL_ADDRESS,
            #             f"get_emails_to_send (URL: {GET_EMAILS_TO_SEND_ENDPOINT})",
            #             self.get_consecutive_fail_count
            #             ),
            #         ]
            
            return []

        self.get_consecutive_fail_count = 0

        response_data = response.json()
        return response_data['result']['emails']
    
    def mark_email_as_sent(self, email_type, receivers_address):
        request_body = {
            'email_type': email_type,
            'email': receivers_address,
        }

        response = requests.post(
            MARK_EMAIL_AS_SENT_ENDPOINT,
            headers=self.request_headers,
            json=request_body
        )

        if response.status_code != 200:
            self.mark_consecutive_fail_count += 1

            logger(response.status_code)
            logger(response.json())

            logger(f"Failed to mark email as sent from endpoint: {MARK_EMAIL_AS_SENT_ENDPOINT}")

            # if self.mark_consecutive_fail_count > ADMIN_EMAIL_FAIL_COUNT_THRESHOLD:
            #     self.mark_consecutive_fail_count = 0
            
            return False

        return True


def main_loop(email_service_handler):
    emails_to_send = email_service_handler.get_emails_to_send()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(SENDERS_EMAIL_ADDRESS, SENDERS_EMAIL_PASSWORD)

        for email_detail in emails_to_send:
            email_message = EmailMessage()

            email_message['From'] = SENDERS_EMAIL_ADDRESS

            email_message['To'] = email_detail['receivers_address']
            email_message['Subject'] = email_detail['subject']

            email_message.set_content(email_detail['plain_text_content'])
            email_message.add_alternative(email_detail['html_content'], subtype='html')

            print(f"Sent email of type {email_detail['type']} to {email_detail['receivers_address']}.")
            print(email_detail['plain_text_content'])
            print()
            print("--------------------------------------------------")
            print()
            print()
            # sleep(2)
            smtp.send_message(email_message)

            email_service_handler.mark_email_as_sent(
                email_detail['type'],
                email_detail['receivers_address']
            )


def main():
    email_service_handler = EmailServiceHandler()

    while True:
        try:
            main_loop(email_service_handler)
        except Exception:
            logger(traceback.format_exc())
        
        sleep(POLL_PERIOD)


if __name__ == "__main__":
    main()
