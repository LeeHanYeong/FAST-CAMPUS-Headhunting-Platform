from django.contrib.auth.views import (
    LogoutView as DjangoLogoutView,
    LoginView as DjangoLoginView,
)
from django.views.generic import TemplateView, ListView

from .forms import LoginForm
from .models import ApplicantUser


class ApplicantListView(ListView):
    model = ApplicantUser
    queryset = ApplicantUser.objects.prefetch_related('followers')
    template_name = 'members/applicant_list.jinja2'
    context_object_name = 'applicants'


class ApplicantUpdateView(TemplateView):
    template_name = 'members/applicant_update.jinja2'


class LoginView(DjangoLoginView):
    form_class = LoginForm
    template_name = 'members/login.html'


class LogoutView(DjangoLogoutView):
    pass
