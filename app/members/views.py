from django.contrib.auth import login
from django.contrib.auth.views import (
    LogoutView as DjangoLogoutView,
    LoginView as DjangoLoginView,
)
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, FormView

from administrator.models import StaticContent
from .forms import LoginForm, ApplicantSignupForm
from .models import ApplicantUser


class ApplicantListView(ListView):
    model = ApplicantUser
    queryset = ApplicantUser.objects.published()\
        .prefetch_related('followers', '_skills')
    template_name = 'members/applicant_list.jinja2'
    context_object_name = 'applicants'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ApplicantUpdateView(TemplateView):
    template_name = 'members/applicant_update.jinja2'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class LoginView(DjangoLoginView):
    form_class = LoginForm
    template_name = 'members/login.jinja2'


class LogoutView(DjangoLogoutView):
    pass


class SignupView(TemplateView):
    template_name = 'members/signup.jinja2'


class ApplicantSignupView(FormView):
    form_class = ApplicantSignupForm
    template_name = 'members/signup_applicant.jinja2'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        static_content = StaticContent.objects.first()
        if not StaticContent.objects.exists():
            static_content = StaticContent.objects.create()
        context['static_content'] = static_content
        return context
