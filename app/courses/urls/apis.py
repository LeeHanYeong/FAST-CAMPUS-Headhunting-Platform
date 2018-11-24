from django.urls import path

from .. import apis

app_name = 'courses'
urlpatterns = [
    path('category/',
         apis.JobCategoryListAPIView.as_view(),
         name='job-category-list'),
]
