from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from ..models import Education, Career, License

User = get_user_model()

__all__ = (
    'ApplicantUserAdmin',
)


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
    list_display = ('name',)
    list_filter = ()
    ordering = ('pk',)

    inlines = [
        EducationInline,
        CareerInline,
        LicenseInline,
    ]
    fieldsets = (
        (None, {'fields': (
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
        ('추가정보', {'fields': (
            'is_looking',
            'short_intro',
            'introduce',
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

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['type'].choices = [User.CHOICES_TYPE[0]]
        if obj:
            form.base_fields['type'].disabled = True
        return form
