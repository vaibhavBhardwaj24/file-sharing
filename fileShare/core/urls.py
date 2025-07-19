from django.urls import path
from core.views.auth_views import  ClientLoginView, ClientSignupView,AccountActivation
from core.views.file_views import DownloadFile, UploadFileView,GenerateFileLink,GetAllFiles
from core.views.test_views import TestView
urlpatterns = [
    path('auth/login/',ClientLoginView.as_view(), name='login'),
    path('auth/signup/',ClientSignupView.as_view(), name='signup'),
    # path('auth/admin/',OperatorLoginView.as_view(), name='admin'),
    path('file/upload/',UploadFileView.as_view(), name='upload'),
    path('file/generateLink/',GenerateFileLink.as_view(),name='generateLink'),
    path('media/<str:file_id>/',DownloadFile.as_view(),name='download'),
    path('links/',GetAllFiles.as_view(),name="links"),
    path('test/',TestView.as_view(), name='test'),
    path('verify-email/<str:token>/',AccountActivation.as_view(), name='verify-email'),  
]
