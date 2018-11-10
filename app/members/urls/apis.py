from django.urls import path

from .. import apis

urlpatterns = [
    path('applicant/<int:pk>/', apis.ApplicantUserRetrieveUpdateAPIView.as_view()),
    path('applicant/link/', apis.ApplicantLinkListCreateAPIView.as_view()),
    path('applicant/skill/', apis.ApplicantSkillListCreateAPIView.as_view()),
]
