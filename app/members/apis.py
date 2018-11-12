from rest_framework import generics, permissions

from .models import (
    ApplicantUser,
    ApplicantLink,
    ApplicantSkill,
    Link, Skill)
from .permissions import ObjIsRequestUser
from .serializers import (
    ApplicantLinkSerializer,
    ApplicantLinkCreateSerializer,
    ApplicantSkillCreateSerializer,
    LinkSerializer, SkillSerializer)
from .serializers import (
    ApplicantUserSerializer,
    ApplicantSkillSerializer,
)


class ApplicantUserUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = ApplicantUser.objects.prefetch_related(
        'education_set',
        'career_set',
        'license_set',
    )
    serializer_class = ApplicantUserSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        ObjIsRequestUser,
    )

    def get_object(self):
        return self.queryset.get(pk=self.request.user.pk)


class ApplicantUserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = ApplicantUser.objects.prefetch_related(
        'education_set',
        'career_set',
        'license_set',
    )
    serializer_class = ApplicantUserSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get_object(self):
        return self.queryset.get(pk=self.request.user.pk)


class LinkListAPIView(generics.ListAPIView):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer


class SkillListAPIView(generics.ListAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


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
