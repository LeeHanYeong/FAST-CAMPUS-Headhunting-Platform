from rest_framework import generics, permissions

from .models import (
    ApplicantUser,
    ApplicantLink,
    ApplicantSkill,
    Link, Skill)
from .serializers import (
    ApplicantLinkSerializer,
    ApplicantLinkCreateSerializer,
    ApplicantSkillCreateSerializer,
    LinkSerializer, SkillSerializer)
from .serializers import (
    ApplicantUserSerializer,
    ApplicantSkillSerializer,
)
from .permissions import ObjIsRequestUserOrReadOnly


class ApplicantUserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = ApplicantUser.objects.prefetch_related(
        'education_set',
        'career_set',
        'license_set',
    )
    serializer_class = ApplicantUserSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        ObjIsRequestUserOrReadOnly,
    )

    def get_object(self):
        # /applicant/profile/ 접속 시 request.user를 retrieve
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        if lookup_url_kwarg not in self.kwargs and self.request.user.is_authenticated:
            self.kwargs[lookup_url_kwarg] = getattr(self.request.user, self.lookup_field)
        return super().get_object()



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
