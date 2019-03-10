from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from ..models import Education, Career, License, ApplicantLink, ApplicantSkill

User = get_user_model()

__all__ = (
    'ApplicantUserAdmin',
)


class ApplicantLinkInline(admin.TabularInline):
    model = ApplicantLink
    extra = 1


class ApplicantSkillInline(admin.TabularInline):
    model = ApplicantSkill
    extra = 1


class EducationInline(admin.TabularInline):
    model = Education
    extra = 1


class CareerInline(admin.TabularInline):
    model = Career
    extra = 1


class LicenseInline(admin.TabularInline):
    model = License
    extra = 1


class ApplicantUserAdmin(BaseUserAdmin):
    list_display = ('name', 'is_active', 'email', 'phone_number', 'birth_date',)
    list_filter = ('is_active',)
    search_fields = ('name',)
    ordering = ('pk',)
    readonly_fields = ('is_active',)
    actions = ['activate']

    inlines = [
        EducationInline,
        CareerInline,
        LicenseInline,
        ApplicantLinkInline,
        ApplicantSkillInline,
    ]
    fieldsets = (
        (None, {'fields': (
            'is_active',
            'type',
            'email',
            'password',
        )}),
        ('개인정보', {'fields': (
            'last_name',
            'first_name',
            'phone_number',
            'birth_date',
            'img_profile',
        )}),
        ('지원자 정보', {'fields': (
            'is_published',
            'is_looking',
            'short_intro',
            'introduce',
            'job_groups',
            'pdf1',
            'pdf2',
        )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'type',
                'email',
                'password1',
                'password2',
            )
        }),
        ('개인정보', {'fields': (
            'last_name',
            'first_name',
            'phone_number',
            'birth_date',
        )}),
    )

    def activate(self, request, queryset):
        for user in queryset:
            user.send_signup_approve()
            user.is_active = True
            user.save()

    activate.short_description = '활성화 처리'

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['type'].choices = [User.CHOICES_TYPE[0]]
        if obj:
            form.base_fields['type'].disabled = True
        return form
