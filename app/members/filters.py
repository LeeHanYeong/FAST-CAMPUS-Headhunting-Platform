import django_filters

from .models import ApplicantUser


class ApplicantUserFilter(django_filters.FilterSet):
    class Meta:
        model = ApplicantUser
        fields = {
            'is_looking': [
                'exact',
            ],
        }
