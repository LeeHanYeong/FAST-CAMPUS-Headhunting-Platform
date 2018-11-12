from django.urls import path

from .. import views

app_name = 'members'
urlpatterns = [
    path('applicant/<int:pk>/', views.ApplicantUpdateView.as_view(), name='applicant-update'),
]
