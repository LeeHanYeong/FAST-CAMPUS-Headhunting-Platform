from .models import JobCategory, JobGroup


def job(request):
    category_list = JobCategory.objects.all()
    group_list = JobGroup.objects.all()
    return {
        'category_list': category_list,
        'group_list': group_list,
    }
