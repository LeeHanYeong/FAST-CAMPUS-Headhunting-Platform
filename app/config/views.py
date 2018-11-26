import json

from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView

from administrator.mixins import StaticContentMixin


class IndexView(StaticContentMixin, TemplateView):
    template_name = 'index.jinja2'


class HealthCheck(View):
    def get(self, request):
        data = {
            'status': 'healthy',
        }
        return HttpResponse(json.dumps(data))
