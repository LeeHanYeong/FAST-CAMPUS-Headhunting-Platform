from django.contrib.auth.views import (
    LogoutView as DjangoLogoutView,
    LoginView as DjangoLoginView,
)
from django.views.generic import TemplateView, ListView

from .forms import LoginForm
from .models import ApplicantUser


class ApplicantListView(ListView):
    model = ApplicantUser
    queryset = ApplicantUser.objects.published().prefetch_related('followers')
    template_name = 'members/applicant_list.jinja2'
    context_object_name = 'applicants'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['form'] =
        return context


class ApplicantUpdateView(TemplateView):
    template_name = 'members/applicant_update.jinja2'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class LoginView(DjangoLoginView):
    form_class = LoginForm
    template_name = 'members/login.html'


class LogoutView(DjangoLogoutView):
    pass
