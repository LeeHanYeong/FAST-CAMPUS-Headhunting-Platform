from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, ApplicantUser, CompanyUser, Link, Skill


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


class ApplicantUserAdmin(BaseUserAdmin):
    list_display = ('name',)
    list_filter = ()
    ordering = ('pk',)

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
        )}),
        ('추가정보', {'fields': (
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

    def get_changeform_initial_data(self, request):
        return {
            'phone_number': '+82-010-',
        }


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


admin.site.register(ApplicantUser, ApplicantUserAdmin)
admin.site.register(CompanyUser, CompanyUserAdmin)
admin.site.register(Link)
admin.site.register(Skill)
