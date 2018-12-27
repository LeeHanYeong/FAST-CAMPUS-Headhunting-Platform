from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .applicant import ApplicantUserAdmin
from ..models import User, ApplicantUser, CompanyUser, Link, Skill, CompanyUserHireJobGroupWithApprovalStatus


class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'last_name', 'first_name', 'is_staff')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('type', 'email', 'password', 'phone_number')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )


class CompanyUserAdmin(BaseUserAdmin):
    list_display = ('name', '_company_name', '_position',)
    list_filter = ()
    ordering = ('pk',)

    fieldsets = (
        (None, {'fields': (
            'type',
            'email',
            'last_name',
            'first_name',
            'password',
            'phone_number',
            '_company_name',
            '_position',
        )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'type',
                'email',
                'last_name',
                'first_name',
                'password1',
                'password2',
                '_company_name',
                '_position',
            )
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['type'].choices = [User.CHOICES_TYPE[1]]
        if obj:
            form.base_fields['type'].disabled = True
        return form


admin.site.register(User, UserAdmin)
admin.site.register(ApplicantUser, ApplicantUserAdmin)
admin.site.register(CompanyUser, CompanyUserAdmin)
admin.site.register(CompanyUserHireJobGroupWithApprovalStatus)
admin.site.register(Link)
admin.site.register(Skill)
