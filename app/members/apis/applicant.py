from rest_framework import generics, permissions, status
from rest_framework.response import Response

from ..models import (
    ApplicantUser,
    Link, Skill, ApplicantLink, ApplicantSkill)
from ..permissions.apis import ObjIsRequestUser, IsUserOrReadOnly
from ..serializers import (
    ApplicantLinkSerializer,
    LinkSerializer, SkillSerializer)
from ..serializers import (
    ApplicantUserSerializer,
    ApplicantSkillSerializer,
)

__all__ = (
    'ApplicantUserUpdateAPIView',
    'ApplicantUserRetrieveAPIView',
    'LinkListAPIView',
    'SkillListAPIView',
    'ApplicantLinkListUpdateAPIView',
    'ApplicantSkillListUpdateAPIView',
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


class ApplicantLinkListUpdateAPIView(generics.ListAPIView):
    serializer_class = ApplicantLinkSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsUserOrReadOnly,
    )

    def get_queryset(self):
        return ApplicantLink.objects.filter(user=self.request.user)

    def put(self, request):
        links = ApplicantLink.objects.filter(user=self.request.user)
        serializer = self.serializer_class(
            links, data=request.data, many=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApplicantSkillListUpdateAPIView(generics.ListAPIView):
    serializer_class = ApplicantSkillSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsUserOrReadOnly,
    )

    def get_queryset(self):
        return ApplicantSkill.objects.filter(user=self.request.user)

    def put(self, request):
        skills = ApplicantSkill.objects.filter(user=self.request.user)
        serializer = self.serializer_class(
            skills, data=request.data, many=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
