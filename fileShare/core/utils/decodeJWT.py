
import jwt
from django.conf import settings
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
def decode_jwt_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload
    except ExpiredSignatureError:
        return {'error': 'Token expired'}
    except InvalidTokenError:
        return {'error': 'Invalid token'}