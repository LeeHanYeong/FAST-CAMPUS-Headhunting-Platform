from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.views.generic import TemplateView


class ApplicantUpdateView(TemplateView):
    template_name = 'members/applicant_update.jinja2'


class LogoutView(DjangoLogoutView):
    pass
