from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.forms import CheckboxSelectMultiple

from .models import StaticContent, Company, Service, MailingGroup

User = get_user_model()


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'service', 'url')
    list_editable = ('type', 'service', 'url')


class MailingGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_applied', 'users_display')
    formfield_overrides = {
        models.ManyToManyField: {
            'widget': CheckboxSelectMultiple,
        }
    }

    def users_display(self, obj):
        return ', '.join([user.name for user in obj.users.all()])

    users_display.short_description = '구성원 목록'

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'users':
            kwargs['queryset'] = User.objects.filter(type=User.TYPE_STAFF)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Company, CompanyAdmin)
admin.site.register(Service)
admin.site.register(StaticContent)
admin.site.register(ContentType)
admin.site.register(MailingGroup, MailingGroupAdmin)
