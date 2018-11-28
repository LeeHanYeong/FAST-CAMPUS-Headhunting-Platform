import json

from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView, ListView

from administrator.mixins import StaticContentMixin
from administrator.models import Company


class IndexView(StaticContentMixin, TemplateView):
    template_name = 'index.jinja2'


class CompanyList(ListView):
    model = Company
    template_name = 'company_list.jinja2'
    context_object_name = 'company_list'


class HealthCheck(View):
    def get(self, request):
        data = {
            'status': 'healthy',
        }
        return HttpResponse(json.dumps(data))
