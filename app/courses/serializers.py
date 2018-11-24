from rest_framework import serializers

from .models import JobCategory, JobGroup


class JobGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobGroup
        fields = (
            'pk',
            'title',
        )


class JobCategorySerializer(serializers.ModelSerializer):
    group_set = JobGroupSerializer(many=True)

    class Meta:
        model = JobCategory
        fields = (
            'pk',
            'title',
            'group_set',
        )
