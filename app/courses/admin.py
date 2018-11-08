from django.contrib import admin

from .models import CoursePeriod, Course


class CoursePeriodAdmin(admin.ModelAdmin):
    list_display = ('__str__',)


admin.site.register(Course)
admin.site.register(CoursePeriod, CoursePeriodAdmin)
