from django.http import JsonResponse
from django.contrib.auth.middleware import get_user
from rest_framework.authentication import get_authorization_header
from django.contrib.auth.models import AnonymousUser

from .authentication import decode_jwt
from .exceptions import DecodeTokenError, ExpiredTokenError


def jwt_authentication_middleware(get_response):
    def middleware(request):
        # This is a lazy evaluation of the request user which will only query the user once it is needed.
        auth_header = get_authorization_header(request).decode('utf-8')
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                payload = decode_jwt(token)
                user = type('User', (),
                            {'is_authenticated': True,
                             'is_active': True,
                             'claims': payload.get('claims', []),
                             'roles': payload.get('roles', []),
                             'identity_id': payload.get('id')})

                # Attach claims to the request object
                request.user = user
                
            except DecodeTokenError:
                return JsonResponse({'error': 'Invalid Token'}, status=401)
            
            except ExpiredTokenError:
                return JsonResponse({'error': 'Token has expired'}, status=401)
        else:
            request.user = AnonymousUser()
        
        response = get_response(request)
        return response
    
    return middleware


class DisableCSRFMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)
        response = self.get_response(request)
        return response
    