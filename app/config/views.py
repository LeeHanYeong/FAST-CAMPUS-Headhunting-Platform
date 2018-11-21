from django.views.generic import TemplateView

from administrator.mixins import StaticContentMixin


class IndexView(StaticContentMixin, TemplateView):
    template_name = 'index.jinja2'
