import django_filters

from .models import Company

__all__ = (
    'CompanyFilter',
)


class CompanyFilter(django_filters.FilterSet):
    class Meta:
        model = Company
        fields = {
            'type': [
                'exact',
            ],
            'service': [
                'exact',
            ]
        }
