from rest_framework import generics
from .models import ApplicantUser
from .serializers import ApplicantUserSerializer


class ApplicantUserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = ApplicantUser.objects.all()
    serializer_class = ApplicantUserSerializer
