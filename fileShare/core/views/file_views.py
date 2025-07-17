from django.http.response import FileResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions
# from rest_framework_simplejwt.tokens import RefreshToken
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from datetime import datetime
from core.models.file_model import File
from rest_framework_simplejwt.tokens import AccessToken
from core.utils.decodeJWT import decode_jwt_token
from core.models.user_model import User
import secrets
from django.core.cache import cache
from datetime import timedelta
from django.conf import settings
import mimetypes
class UploadFileView(APIView):
    authentication_classes = [] 

    def post(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return Response({'error': 'Authorization header missing or malformed'}, status=status.HTTP_401_UNAUTHORIZED)
        token = auth_header.split(' ')[1]

        user = decode_jwt_token(token)
        if 'error' in user:
            return Response({'error': user['error']}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.get("is_admin"):
            return Response({'error': 'User is not an operator'}, status=status.HTTP_403_FORBIDDEN)
        
        file=request.FILES.get('file')
        if not file:
            return Response({'error': 'Please provide a file'}, status=status.HTTP_400_BAD_REQUEST)
        
        ext = os.path.splitext(file.name)[1].lower()
        ALLOWED_TYPES=['.docx','.xlsx','.pptx']
        if  ext not in ALLOWED_TYPES:
            return Response({'error': 'Invalid file type'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            now = datetime.now()
            relative_path = default_storage.save(f"uploads/{now.timestamp()}-{file.name}", ContentFile(file.read()))
            newFile=File(uploadedBy=user.get("user_id"),fileName=f"{now.timestamp()}-{file.name}",filePath=relative_path,fileType=ext,uploaded_at=now.date()).save(
                force_insert=True
            )
            return Response({'message': 'File uploaded successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class GenerateFileLink(APIView):
    authentication_classes=[]
    def post(self,request):
        try:
            auth_header = request.headers.get('Authorization')
            file_name= request.data.get('file_name')
            # if file name is not given return error
            if not file_name:
                return Response({'error':'File Name Required'},status=status.HTTP_400_BAD_REQUEST)
            if not auth_header or not auth_header.startswith('Bearer '):
                return Response({'error': 'Authorization header missing or malformed'}, status=status.HTTP_401_UNAUTHORIZED)
            token = auth_header.split(' ')[1]

            decoded = decode_jwt_token(token)
            user=User.objects(uuid=decoded.get("user_id")).first()
             # if user is not found return error
            if not user:
                return Response({'error':'No user found'},status=status.HTTP_404_NOT_FOUND)
            if user.is_admin:
                return Response({'error':'Only client accounts are allowed'},status=status.HTTP_401_UNAUTHORIZED)
            # if not user.is_active:
            #     return Response({'error':'Account not activated'},status=status.HTTP_401_UNAUTHORIZED)
            # if file is not found in mongodb return error
            file=File.objects(fileName=file_name).first()
            if not file:
                return Response({'error':'File not found'},status=status.HTTP_404_NOT_FOUND)
            # generate random file id 
            file_id=secrets.token_urlsafe(8)[:10]
            # store file id and path in redis with TTL 10 min
            cache.set(file_id,file.filePath,600)
            return Response({'message':'link created valid for 10 mins',
                            'link': request.build_absolute_uri(f"/api/media/{file_id}/"),
                            'valid_till': (datetime.now() + timedelta(minutes=10)).strftime('%Y-%m-%d %H:%M:%S')
                            },status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class DownloadFile(APIView):
    def get(self,request,file_id):
        try:
            
            path=cache.get(file_id)
            if not path:
                return Response({'error':'Link Invalid or Expired'},status=status.HTTP_404_NOT_FOUND)
            full_path = os.path.join(settings.MEDIA_ROOT, path)
            if not os.path.exists(full_path):
                return Response({'error':'File not found'},status=status.HTTP_404_NOT_FOUND)
            
            mime_type, _ = mimetypes.guess_type(full_path)
            return FileResponse(open(full_path, 'rb'), content_type=mime_type or 'application/octet-stream', as_attachment=True)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetAllFiles(APIView):
    authentication_classes=[]
    def get(self,request):
        try:
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return Response({'error': 'Authorization header missing or malformed'}, status=status.HTTP_401_UNAUTHORIZED)
            
            token = auth_header.split(' ')[1]

            decoded = decode_jwt_token(token)
            user=User.objects(uuid=decoded.get("user_id")).first()
            if not user:
                return Response({'error':'No user found'},status=status.HTTP_404_NOT_FOUND)
            if user.is_admin:
                return Response({'error':'Only client accounts are allowed'},status=status.HTTP_401_UNAUTHORIZED)
           
            files = File.objects()

            # Serialize files into a list of dicts
            file_list = [
                {
                    "fileName": file.fileName,
                    "fileType": file.fileType,
                    "uploaded_at": file.uploaded_at.strftime('%Y-%m-%d'),
                }
                for file in files
            ]

            return Response({'files': file_list}, status=status.HTTP_200_OK)


        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
