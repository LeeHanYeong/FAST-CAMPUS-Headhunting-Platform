from django.urls import path

from .. import views

app_name = 'members'
urlpatterns = [
    path('applicant/profile/', views.ApplicantUpdateView.as_view(), name='applicant-update'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
