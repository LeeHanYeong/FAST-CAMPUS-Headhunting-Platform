from django.contrib import admin
from django.contrib.contenttypes.models import ContentType

from .models import StaticContent, Company, Service, MailingGroup


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'service', 'url')
    list_editable = ('type', 'service', 'url')


admin.site.register(Company, CompanyAdmin)
admin.site.register(Service)
admin.site.register(StaticContent)
admin.site.register(ContentType)
admin.site.register(MailingGroup)
