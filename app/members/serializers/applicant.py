from django.contrib.auth import get_user_model
from drf_writable_nested import WritableNestedModelSerializer
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from ..models import Education, Career, License, ApplicantLink, Link, ApplicantSkill, Skill

User = get_user_model()

__all__ = (
    'LinkSerializer',
    'SkillSerializer',
    'ApplicantUserSerializer',
    'ApplicantLinkSerializer',
    'ApplicantSkillSerializer',
    'ApplicantSkillCreateSerializer',
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
    phone_number = PhoneNumberField()
    education_set = EducationSerializer(many=True)
    career_set = CareerSerializer(many=True)
    license_set = LicenseSerializer(many=True)

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

            'education_set',
            'career_set',
            'license_set',
        )

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['phone_number'] = instance.phone_number.as_national
        return ret

    def to_internal_value(self, data):
        return data


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
