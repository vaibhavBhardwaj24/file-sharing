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
class UploadFileView(APIView):
    permission_classes = [permissions.IsAuthenticated]  
    def post(self,request):
        token=request.headers.get('Authorization').split(' ')[1]
        if not token:
            return Response({'error': 'Please provide a valid token',}, status=status.HTTP_401_UNAUTHORIZED)
        user=AccessToken(token)
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
            relative_path = default_storage.save(f"uploads/{file.name}-{now.timestamp()}", ContentFile(file.read()))
            newFile=File(uploadedBy=user.user_id,fileName=file.name,filePath=relative_path,fileType=ext,uploaded_at=now.date()).save(
                force_insert=True
            )
            return Response({'message': 'File uploaded successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


    