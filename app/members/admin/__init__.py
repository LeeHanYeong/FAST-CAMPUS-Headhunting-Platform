from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Permission, Group
from django.utils.translation import gettext_lazy as _

from .applicant import *
from .company import *
from ..models import *


class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'last_name', 'first_name', 'is_staff')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email',)

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
        (_('Permissions'), {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        )}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )


class CompanyUserAdmin(BaseUserAdmin):
    list_display = ('name', 'is_active', '_company_name', '_position',)
    list_filter = ('is_active',)
    ordering = ('pk',)
    readonly_fields = ('is_active',)
    actions = ['activate']

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

    def activate(self, request, queryset):
        for user in queryset:
            user.send_signup_approve()
            user.is_active = True
            user.save()

    activate.short_description = '활성화 처리'


class StaffGroupInline(admin.TabularInline):
    model = User.groups.through

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        field = super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'user':
            field.queryset = field.queryset.filter(type=User.TYPE_STAFF)
        return field


class GroupAdmin(admin.ModelAdmin):
    inlines = [
        StaffGroupInline,
    ]
    exclude = ('user_set',)


admin.site.register(User, UserAdmin)
admin.site.register(Permission)
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
admin.site.register(ApplicantUser, ApplicantUserAdmin)
admin.site.register(CompanyUser, CompanyUserAdmin)
admin.site.register(CompanyUserHireJobGroupWithApprovalStatus, CompanyUserHireJobGroupWithApprovalStatusAdmin)
admin.site.register(Link)
admin.site.register(Skill)
