from django.urls import path

from .. import views

app_name = 'members'
urlpatterns = [
    path('applicant/profile/', views.ApplicantUpdateView.as_view(), name='applicant-update'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
