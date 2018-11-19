from django.urls import path

from .. import apis

app_name = 'members'
urlpatterns = [
    path('userlike/', apis.UserLikeCreateDestoryAPIView.as_view(), name='userlike'),
    path('skill/', apis.SkillListAPIView.as_view(), name='skill-list'),
    path('link/', apis.LinkListAPIView.as_view(), name='link-list'),
    path('applicant/profile/', apis.ApplicantUserUpdateAPIView.as_view(), name='profile'),
    path('applicant/<int:pk>/', apis.ApplicantUserRetrieveAPIView.as_view()),
    path('applicant/link/', apis.ApplicantLinkListUpdateAPIView.as_view(), name='applicantlink-list'),
    path('applicant/skill/', apis.ApplicantSkillListCreateAPIView.as_view(), name='applicantskill-list'),
]
