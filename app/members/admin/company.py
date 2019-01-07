from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()

__all__ = (
    'CompanyUserHireJobGroupWithApprovalStatusAdmin',
)


class CompanyUserHireJobGroupWithApprovalStatusAdmin(admin.ModelAdmin):
    list_display = ('company_user', 'job_group', 'status')
    list_editable = ('status',)
    search_fields = ('company_user__name',)
