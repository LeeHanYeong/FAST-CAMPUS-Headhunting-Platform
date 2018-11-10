from django.contrib.auth import get_user_model
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from ..models import Education, Career, License, ApplicantLink, Link, ApplicantSkill, Skill

User = get_user_model()

__all__ = (
    'ApplicantUserSerializer',
    'ApplicantLinkSerializer',
    'ApplicantLinkCreateSerializer',
    'ApplicantSkillSerializer',
    'ApplicantSkillCreateSerializer',
)


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = (
            'pk',
            'start_date',
            'end_date',
            'content',
        )


class CareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Career
        fields = (
            'pk',
            'start_date',
            'end_date',
            'content',
        )


class LicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = License
        fields = (
            'pk',
            'get_date',
            'organization',
            'title',
        )


class ApplicantUserSerializer(WritableNestedModelSerializer):
    education_set = EducationSerializer(many=True)
    career_set = CareerSerializer(many=True)
    license_set = LicenseSerializer(many=True)

    class Meta:
        model = User
        fields = (
            'pk',
            'last_name',
            'first_name',
            'email',

            'education_set',
            'career_set',
            'license_set',
        )


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = (
            'pk',
            'title',
            'img_icon',
        )


class ApplicantLinkSerializer(serializers.ModelSerializer):
    link = LinkSerializer(read_only=True)

    class Meta:
        model = ApplicantLink
        fields = (
            'pk',
            'link',
            'url',
        )


class ApplicantLinkCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicantLink
        fields = (
            'pk',
            'link',
            'url',
        )


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = (
            'pk',
            'title',
        )


class ApplicantSkillSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(read_only=True)

    class Meta:
        model = ApplicantSkill
        fields = (
            'pk',
            'skill',
            'level',
        )


class ApplicantSkillCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicantSkill
        fields = (
            'pk',
            'skill',
            'level',
        )
