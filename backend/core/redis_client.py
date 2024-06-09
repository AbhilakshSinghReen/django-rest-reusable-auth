from datetime import datetime
from json import dumps as json_dumps, loads as json_loads

from redis import Redis

from backend_app.settings import (
    REDIS_HOST,
    REDIS_PORT,
    REDIS_DB,
    REDIS_PASSWORD,
)


redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD, decode_responses=True)
password_reset_via_email_requests_set_name = "password_reset_via_email_requests"
blacklisted_tokens_set_name = "blacklisted_tokens"


def add_password_reset_via_email_request(email):
    redis_client.sadd(password_reset_via_email_requests_set_name, email)


def get_password_reset_via_email_requests():
    return redis_client.smembers(password_reset_via_email_requests_set_name)


def remove_password_reset_via_email_request(email):
    redis_client.srem(password_reset_via_email_requests_set_name, email)


def remove_expired_blacklisted_tokens():
    blacklisted_tokens = redis_client.smembers(blacklisted_tokens_set_name)

    for token_with_expiry in blacklisted_tokens:
        try:
            token_expiry_timestamp = json_loads(token_with_expiry)['expiry_timestamp']
            if token_expiry_timestamp <= datetime.now().timestamp():
                redis_client.srem(blacklisted_tokens_set_name, token_with_expiry)
        except:
            redis_client.srem(blacklisted_tokens_set_name, token_with_expiry)


def blacklist_token(token, expiry_timestamp):
    token_with_expiry = {
        'token': token,
        'expiry_timestamp': expiry_timestamp,
    }
    token_with_expiry_str = json_dumps(token_with_expiry)
    
    redis_client.sadd(blacklisted_tokens_set_name, token_with_expiry_str)
    remove_expired_blacklisted_tokens()


def check_if_token_is_blacklisted(token, expiry_timestamp):
    token_with_expiry = {
        'token': token,
        'expiry_timestamp': expiry_timestamp,
    }
    token_with_expiry_str = json_dumps(token_with_expiry)
    
    remove_expired_blacklisted_tokens()
    return redis_client.sismember(blacklisted_tokens_set_name, token_with_expiry_str)
