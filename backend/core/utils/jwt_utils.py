from datetime import datetime

from jwt import (
    decode as jwt_decode,
    encode as jwt_encode,
    ExpiredSignatureError,
    InvalidTokenError,
)

from backend_app.settings import SECRET_KEY


def generate_jwt(payload, expiry_timedelta):
    expiry = datetime.now() + expiry_timedelta
    payload['exp'] = expiry
    token = jwt_encode(payload, SECRET_KEY, algorithm='HS256')
    return token


def verify_jwt(token_str):
    try:
        payload = jwt_decode(token_str, SECRET_KEY, algorithms=['HS256'])

        if 'exp' in payload and datetime.now() > datetime.fromtimestamp(payload['exp']):
            raise ExpiredSignatureError("Token has expired")
        
        return True, payload
    except ExpiredSignatureError:
        return False, "expired"
    except InvalidTokenError:
        return False, "invalid"
