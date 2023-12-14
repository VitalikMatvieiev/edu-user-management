from django.http import JsonResponse
from rest_framework.authentication import get_authorization_header

from .authentication import decode_jwt
from .exceptions import DecodeTokenError, ExpiredTokenError


def jwt_authentication_middleware(get_response):
    def middleware(request):
        auth_header = get_authorization_header(request).decode('utf-8')
        
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                payload = decode_jwt(token)
                
            except DecodeTokenError:
                return JsonResponse({'error': 'Invalid Token'}, status=401)
            
            except ExpiredTokenError:
                return JsonResponse({'error': 'Token has expired'}, status=401)
    
        return get_response(request)
    
    return middleware
    