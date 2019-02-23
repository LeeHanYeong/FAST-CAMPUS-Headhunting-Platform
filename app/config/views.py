import json

from django.contrib import messages
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView, ListView

from administrator.filters import CompanyFilter
from administrator.mixins import StaticContentMixin
from administrator.models import Company, Service


class IndexView(StaticContentMixin, TemplateView):
    template_name = 'index.jinja2'

    def render_to_response(self, context, **response_kwargs):
        messages.success(self.request, 'Index success')
        return super().render_to_response(context, **response_kwargs)


class CompanyList(StaticContentMixin, ListView):
    model = Company
    queryset = Company.objects.select_related('service')
    template_name = 'company_list.jinja2'
    context_object_name = 'company_list'

    def get_queryset(self):
        return CompanyFilter(self.request.GET, queryset=self.queryset).qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['choices_company_type'] = Company.CHOICES_TYPE
        context['service_list'] = Service.objects.all()
        return context


class HealthCheck(View):
    def get(self, request):
        data = {
            'status': 'healthy',
        }
        return HttpResponse(json.dumps(data))
