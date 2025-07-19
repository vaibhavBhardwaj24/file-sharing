from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from core.models.user_model import User
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken 
import jwt
from datetime import datetime, timedelta
from django.conf import settings
import secrets
from django.core.cache import cache
from core.tasks import sendVerificationMail

def tokens_for_user(user):
    access_payload = {
        'user_id': str(user.uuid),  # Use .id, which is a UUID
        'username': user.username,
        'email': user.email,
        'is_admin': user.is_admin,
        'exp': int((datetime.utcnow() + timedelta(minutes=600)).timestamp()),
        'type': 'access'
    }

    refresh_payload = {
        'user_id': str(user.uuid),
        'exp': int((datetime.utcnow() + timedelta(days=7)).timestamp()),
        'type': 'refresh'
    }

    access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm='HS256')
    refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm='HS256')

    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }


class ClientSignupView(APIView):
    authentication_classes=[]
    def post(self, request):
        email=request.data.get('email')
        password=request.data.get('password')
        username=request.data.get('username')

        if not email or not password or not username:
            return Response({'error': 'Please provide email, password and username'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects(email=email).first():
            return Response({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects(username=username).first():
            return Response({'error': 'Username taken'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            hashed_password = make_password(password)
            User(email=email, password_hashed=hashed_password, username=username,is_admin=False,is_active=False).save()
            token = secrets.token_urlsafe(8)[:10]  
            cache.set(token,email,600)
            sendVerificationMail.delay(email,token)
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ClientLoginView(APIView):
    authentication_classes=[]
    def post(self,request):
        email=request.data.get('email')
        password=request.data.get('password')

        if not email or not password:
            return Response({'error': 'Please provide email and password'}, status=status.HTTP_400_BAD_REQUEST)
        
        user=User.objects(email=email).first()
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if not check_password(password,user.password_hashed):
            return Response({'error': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)
        
        tokens = tokens_for_user(user)   
        role = "operator" if user.is_admin else "client"
        return Response({
            'message': 'Login successful',
            'access_token':tokens.get('access_token'),
            'refresh_token':tokens.get('refresh_token'),
            'role':role}, status=status.HTTP_200_OK)

class AccountActivation(APIView):
    def post(self,request,token):
        # token=data
        email=cache.get(token)
        if not email:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        user=User.objects(email=email).first()
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        user.is_active=True
        user.save()
        return Response({'message': 'Account verified successfully'}, status=status.HTTP_200_OK)
