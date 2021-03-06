from django.urls import path

from .. import views

app_name = 'members'
urlpatterns = [
    path('applicants/', views.ApplicantListView.as_view(), name='applicant-list'),
    path('applicants/resume/', views.ApplicantUpdateView.as_view(), name='applicant-update'),
    path('applicants/<int:pk>/', views.ApplicantDetailView.as_view(), name='applicant-detail'),
    path('applicants/profile/', views.ApplicantProfileView.as_view(), name='applicant-profile'),
    path('company-user/profile/', views.CompanyUserProfileView.as_view(), name='company-user-profile'),
    path('company-user/hire-job-groups/', views.CompanyUserHireJobGroupAddRequestView.as_view(), name='hire-job-group'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('signup/applicant/', views.ApplicantSignupView.as_view(), name='applicant-signup'),
    path('signup/company/', views.CompanySignupView.as_view(), name='company-signup'),

    path('password-change/', views.PasswordChangeView.as_view(), name='password-change'),
    path('password-change/done/', views.PasswordChangeDoneView.as_view(), name='password-change-done'),
    path('password-reset/', views.PasswordResetView.as_view(), name='password-reset'),
    path('password-reset/done/', views.PasswordResetDoneView.as_view(), name='password-reset-done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password-reset-complete'),
]
