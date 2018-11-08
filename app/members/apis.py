from rest_framework import generics
from .models import ApplicantUser
from .serializers import ApplicantUserSerializer


class ApplicantUserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = ApplicantUser.objects.prefetch_related(
        'education_set',
        'career_set',
        'license_set',
    )
    serializer_class = ApplicantUserSerializer
