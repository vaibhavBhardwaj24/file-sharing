from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import jwt
from django.conf import settings
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from rest_framework.permissions import AllowAny

def decode_jwt_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload
    except ExpiredSignatureError:
        return {'error': 'Token expired'}
    except InvalidTokenError:
        return {'error': 'Invalid token'}

class TestView(APIView):
    authentication_classes = [] 

    def get(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return Response({'error': 'Authorization header missing'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            token = auth_header.split(' ')[1]
        except IndexError:
            return Response({'error': 'Malformed Authorization header'}, status=status.HTTP_400_BAD_REQUEST)

        payload = decode_jwt_token(token)

        if 'error' in payload:
            return Response({'error': payload['error']}, status=status.HTTP_401_UNAUTHORIZED)

        print(payload)  # Reaches here if valid token
        return Response({'message': 'Hello, world!', 'user': payload}, status=status.HTTP_200_OK)
