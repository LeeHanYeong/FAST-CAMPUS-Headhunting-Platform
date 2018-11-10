from rest_framework import generics, permissions

from .models import (
    ApplicantUser,
    ApplicantLink,
    ApplicantSkill,
)
from .serializers import (
    ApplicantLinkSerializer,
    ApplicantLinkCreateSerializer,
    ApplicantSkillCreateSerializer
)
from .serializers import (
    ApplicantUserSerializer,
    ApplicantSkillSerializer,
)


class ApplicantUserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = ApplicantUser.objects.prefetch_related(
        'education_set',
        'career_set',
        'license_set',
    )
    serializer_class = ApplicantUserSerializer


class ApplicantLinkListCreateAPIView(generics.ListCreateAPIView):
    queryset = ApplicantLink.objects.all()
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ApplicantLinkSerializer
        elif self.request.method == 'POST':
            return ApplicantLinkCreateSerializer


class ApplicantSkillListCreateAPIView(generics.ListCreateAPIView):
    queryset = ApplicantSkill.objects.all()
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ApplicantSkillSerializer
        elif self.request.method == 'POST':
            return ApplicantSkillCreateSerializer
