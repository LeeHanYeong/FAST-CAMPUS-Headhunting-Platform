import django_filters
from django.db.models import Q

from courses.models import JobGroup
from .models import ApplicantUser


class ApplicantUserFilter(django_filters.FilterSet):
    groups = django_filters.ModelMultipleChoiceFilter(
        field_name='job_groups__id',
        to_field_name='id',
        lookup_expr='in',
        queryset=JobGroup.objects.all(),
    )
    keyword = django_filters.CharFilter(
        method='filter_name_keyword',
    )

    class Meta:
        model = ApplicantUser
        fields = {
            'is_looking': [
                'exact',
            ],
        }

    def filter_name_keyword(self, queryset, name, value):
        return queryset.filter(
            Q(full_name__icontains=value) | Q(_skills__title__icontains=value)
        )
