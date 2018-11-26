import django_filters

from courses.models import JobGroup
from .models import ApplicantUser


class ApplicantUserFilter(django_filters.FilterSet):
    groups = django_filters.ModelMultipleChoiceFilter(
        field_name='job_groups__id',
        to_field_name='id',
        lookup_expr='in',
        queryset=JobGroup.objects.all(),
    )

    class Meta:
        model = ApplicantUser
        fields = {
            'is_looking': [
                'exact',
            ]
        }
