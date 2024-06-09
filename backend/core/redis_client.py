from redis import Redis

from backend_app.settings import (
    REDIS_HOST,
    REDIS_PORT,
    REDIS_DB,
    REDIS_PASSWORD,
)


redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD, decode_responses=True)
password_reset_via_email_requests_set_name = "password_reset_via_email_requests"


def add_password_reset_via_email_request(email):
    redis_client.sadd(password_reset_via_email_requests_set_name, email)


def get_password_reset_via_email_requests():
    return redis_client.smembers(password_reset_via_email_requests_set_name)


def remove_password_reset_via_email_request(email):
    redis_client.srem(password_reset_via_email_requests_set_name, email)
