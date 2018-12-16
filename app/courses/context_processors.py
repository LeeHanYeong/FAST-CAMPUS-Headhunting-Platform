from .models import JobCategory, JobGroup


def job(request):
    category_list = JobCategory.objects.all()
    return {
        'category_list': category_list,
    }
