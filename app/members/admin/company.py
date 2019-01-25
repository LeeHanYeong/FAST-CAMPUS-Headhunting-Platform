from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()

__all__ = (
    'CompanyUserHireJobGroupWithApprovalStatusAdmin',
)


class CompanyUserHireJobGroupWithApprovalStatusAdmin(admin.ModelAdmin):
    list_display = ('company_user', 'job_group', 'status')
    list_editable = ('status',)
    list_filter = ('status',)
    actions = [
        'set_status_wait',
        'set_status_approve',
    ]

    def set_status_wait(self, request, queryset):
        from ..models import CompanyUserHireJobGroupWithApprovalStatus
        queryset.update(status=CompanyUserHireJobGroupWithApprovalStatus.STATUS_WAIT)

    set_status_wait.short_description = '승인대기 처리'

    def set_status_approve(self, request, queryset):
        from ..models import CompanyUserHireJobGroupWithApprovalStatus
        queryset.update(status=CompanyUserHireJobGroupWithApprovalStatus.STATUS_APPROVAL)

    set_status_approve.short_description = '승인완료 처리'
