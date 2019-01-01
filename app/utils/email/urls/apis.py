from django.urls import path

from .. import apis

app_name = 'email'
urlpatterns = [
    path('hire/', apis.HireEmailSendAPIView.as_view(), name='hire'),
]
