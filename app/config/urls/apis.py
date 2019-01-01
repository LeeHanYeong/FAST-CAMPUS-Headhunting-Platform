from django.urls import include, path

app_name = 'api'
urlpatterns = [
    path('members/', include('members.urls.apis')),
    path('courses/', include('courses.urls.apis')),
    path('email/', include('utils.email.urls.apis')),
]
