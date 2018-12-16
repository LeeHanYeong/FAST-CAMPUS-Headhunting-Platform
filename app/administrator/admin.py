from django.contrib import admin

from .models import StaticContent, Company, Service


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'service', 'url')
    list_editable = ('type', 'service', 'url')
    # sortable_by = ('name',)


admin.site.register(Company, CompanyAdmin)
admin.site.register(Service)
admin.site.register(StaticContent)
