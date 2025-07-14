from django.urls import path
from core.views.auth_views import OperatorLoginView, ClientLoginView, ClientSignupView
from core.views.file_views import UploadFileView
from core.views.test_views import TestView
urlpatterns = [
    path('auth/login/',ClientLoginView.as_view(), name='login'),
    path('auth/signup/',ClientSignupView.as_view(), name='signup'),
    path('auth/admin/',OperatorLoginView.as_view(), name='admin'),
    path('file/upload',UploadFileView.as_view(), name='upload'),
    path('test/',TestView.as_view(), name='test'),
]
