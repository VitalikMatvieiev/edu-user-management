import jwt
from django.conf import settings
from .exceptions import DecodeTokenError, ExpiredTokenError
import logging

logger = logging.getLogger(__name__)


def decode_jwt(token):

    try:
        decode_payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
        return decode_payload
    
    except jwt.DecodeError:
        # logger.info('Token is invalid', exc_info=True)
        raise DecodeTokenError('Token is invalid')
    
    except jwt.ExpiredSignatureError:
        # logger.info('Signature is expired', exc_info=True)
        raise ExpiredTokenError('Signature has expired')
