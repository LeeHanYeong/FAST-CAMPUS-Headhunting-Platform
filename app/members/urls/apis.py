from django.urls import path

from .. import apis

urlpatterns = [
    path('skill/', apis.SkillListAPIView.as_view()),
    path('link/', apis.LinkListAPIView.as_view()),
    path('applicant/profile/', apis.ApplicantUserRetrieveUpdateAPIView.as_view()),
    path('applicant/<int:pk>/', apis.ApplicantUserRetrieveUpdateAPIView.as_view()),
    path('applicant/link/', apis.ApplicantLinkListCreateAPIView.as_view()),
    path('applicant/skill/', apis.ApplicantSkillListCreateAPIView.as_view()),
]
