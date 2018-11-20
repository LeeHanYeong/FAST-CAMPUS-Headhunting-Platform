from django.urls import path

from .. import views

app_name = 'members'
urlpatterns = [
    path('applicant/', views.ApplicantListView.as_view(), name='applicant-list'),
    path('applicant/profile/', views.ApplicantUpdateView.as_view(), name='applicant-update'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('signup/applicant/', views.ApplicantSignupView.as_view(), name='applicant-signup'),
]
