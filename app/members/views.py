from django.contrib.auth.views import (
    LogoutView as DjangoLogoutView,
    LoginView as DjangoLoginView,
)
from django.views.generic import TemplateView
from .forms import LoginForm


class ApplicantUpdateView(TemplateView):
    template_name = 'members/applicant_update.jinja2'


class LoginView(DjangoLoginView):
    form_class = LoginForm
    template_name = 'members/login.html'


class LogoutView(DjangoLogoutView):
    pass
