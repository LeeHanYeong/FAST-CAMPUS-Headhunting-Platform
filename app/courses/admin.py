from django.contrib import admin

from .models import JobCategory, JobGroup, CoursePeriod, Course


class CoursePeriodAdmin(admin.ModelAdmin):
    list_display = ('__str__',)


admin.site.register(JobCategory)
admin.site.register(JobGroup)
admin.site.register(Course)
admin.site.register(CoursePeriod, CoursePeriodAdmin)
