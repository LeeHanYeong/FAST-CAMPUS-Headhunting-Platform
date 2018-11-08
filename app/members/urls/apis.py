from django.urls import path

from .. import apis

urlpatterns = [
    path('applicant/<pk>/', apis.ApplicantUserRetrieveUpdateAPIView.as_view()),
]
