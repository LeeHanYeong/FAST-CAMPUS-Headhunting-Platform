from django.contrib.auth import get_user_model
from drf_writable_nested import WritableNestedModelSerializer
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from courses.serializers import JobGroupSerializer
from ..models import (
    Education,
    Career,
    License,
    ApplicantLink,
    Link,
    ApplicantSkill,
    Skill,
    ApplicantUser
)

User = get_user_model()

__all__ = (
    'LinkSerializer',
    'SkillSerializer',
    'ApplicantUserSerializer',
    'ApplicantLinkSerializer',
    'ApplicantSkillSerializer',
)


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = (
            'pk',
            'school',
            'major',
            'type',
            'start_date',
            'end_date',
        )

    def to_internal_value(self, data):
        if data['end_date'] == '':
            data.pop('end_date')
        return data


class CareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Career
        fields = (
            'pk',
            'organization',
            'responsibility',
            'position',
            'start_date',
            'end_date',
        )

    def to_internal_value(self, data):
        if data['end_date'] == '':
            data.pop('end_date')
        return data


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
    phone_number = PhoneNumberField()
    education_set = EducationSerializer(many=True)
    career_set = CareerSerializer(many=True)
    license_set = LicenseSerializer(many=True)
    job_groups = JobGroupSerializer(many=True)
    choices_looking = serializers.SerializerMethodField()
    choices_type = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'pk',
            'is_looking',
            'is_published',
            'img_profile',
            'last_name',
            'first_name',
            'email',
            'phone_number',
            'birth_date',
            'short_intro',
            'introduce',
            'pdf1',
            'pdf2',

            'education_set',
            'career_set',
            'license_set',
            'job_groups',

            'choices_looking',
            'choices_type',
        )

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['phone_number'] = instance.phone_number.as_national if instance.phone_number else ''
        return ret

    def to_internal_value(self, data):
        return data

    def get_choices_looking(self, obj):
        return ApplicantUser.CHOICES_LOOKING

    def get_choices_type(self, obj):
        return ApplicantUser.CHOICES_TYPE


class LinkSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField()

    class Meta:
        model = Link
        fields = (
            'pk',
            'title',
            'img_icon',
        )
        read_only_fields = (
            'img_icon',
        )


class ApplicantLinkListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        link_mapping = {link.pk: link for link in instance}

        updated = []
        created = []
        # 전달받은 validate_date의 pk에 포함되지 않는 기존 ApplicantLink는 모두 삭제한다
        #  (항상 기존/수정/추가에 해당하는 전체 데이터가 올 것으로 가정)
        # created에는 'pk'가 전달되지 않은(추가할 새 데이터) 새 인스턴스를 저장
        for data in validated_data:
            data_pk = data.get('pk')
            if data_pk:
                link = link_mapping.get(data_pk)
                if link:
                    updated.append(self.child.update(link, data))
            else:
                created.append(self.child.create(data))

        # 삭제루틴
        updated_pk_list = [item.pk for item in updated]
        for link_id, link in link_mapping.items():
            if link_id not in updated_pk_list:
                link.delete()
        return updated + created


class ApplicantLinkSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(required=False)
    link = LinkSerializer()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ApplicantLink
        list_serializer_class = ApplicantLinkListSerializer
        fields = (
            'pk',
            'link',
            'url',
            'user',
        )
        read_only_fields = (
            'user',
        )

    def create(self, validated_data):
        link_data = validated_data.pop('link')
        link = get_object_or_404(Link, pk=link_data['pk'])
        return ApplicantLink.objects.create(link=link, **validated_data)

    def update(self, instance, validated_data):
        link_data = validated_data.pop('link')
        link = get_object_or_404(Link, pk=link_data['pk'])
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.link = link
        instance.save()
        return instance


class SkillSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField()

    class Meta:
        model = Skill
        fields = (
            'pk',
            'title',
        )


class ApplicantSkillListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        obj_mapping = {obj.pk: obj for obj in instance}

        updated = []
        created = []
        # 전달받은 validate_date의 pk에 포함되지 않는 기존 ApplicantLink는 모두 삭제한다
        #  (항상 기존/수정/추가에 해당하는 전체 데이터가 올 것으로 가정)
        # created에는 'pk'가 전달되지 않은(추가할 새 데이터) 새 인스턴스를 저장
        for data in validated_data:
            data_pk = data.get('pk')
            if data_pk:
                obj = obj_mapping.get(data_pk)
                if obj:
                    updated.append(self.child.update(obj, data))
            else:
                created.append(self.child.create(data))

        # 삭제루틴
        updated_pk_list = [item.pk for item in updated]
        for obj_id, obj in obj_mapping.items():
            if obj_id not in updated_pk_list:
                obj.delete()
        return updated + created


class ApplicantSkillSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(required=False)
    skill = SkillSerializer()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ApplicantSkill
        list_serializer_class = ApplicantSkillListSerializer
        fields = (
            'pk',
            'skill',
            'level',
            'get_level_display',
            'user',
        )
        read_only_fields = (
            'user',
        )

    def create(self, validated_data):
        skill_data = validated_data.pop('skill')
        skill = get_object_or_404(Skill, pk=skill_data['pk'])
        return ApplicantSkill.objects.create(skill=skill, **validated_data)

    def update(self, instance, validated_data):
        skill_data = validated_data.pop('skill')
        skill = get_object_or_404(Skill, pk=skill_data['pk'])
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.skill = skill
        instance.save()
        return instance
