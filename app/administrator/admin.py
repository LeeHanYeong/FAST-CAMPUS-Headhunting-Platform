from django.contrib import admin

from .models import StaticContent, Company

admin.site.register(Company)
admin.site.register(StaticContent)
