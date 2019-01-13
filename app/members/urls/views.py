from django.urls import path

from .. import views

app_name = 'members'
urlpatterns = [
    path('applicants/', views.ApplicantListView.as_view(), name='applicant-list'),
    path('applicants/profile/', views.ApplicantUpdateView.as_view(), name='applicant-update'),
    path('applicants/<int:pk>/', views.ApplicantDetailView.as_view(), name='applicant-detail'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('signup/applicant/', views.ApplicantSignupView.as_view(), name='applicant-signup'),
    path('signup/company/', views.CompanySignupView.as_view(), name='company-signup'),
]
