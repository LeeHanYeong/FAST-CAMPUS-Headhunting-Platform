from django.contrib.auth import login
from django.contrib.auth.views import (
    LogoutView as DjangoLogoutView,
    LoginView as DjangoLoginView,
)
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, FormView, DetailView

from administrator.mixins import StaticContentMixin
from .filters import ApplicantUserFilter
from .forms import LoginForm, ApplicantSignupForm, CompanySignupForm
from .models import ApplicantUser, ApplicantSkill


class ApplicantListView(ListView):
    model = ApplicantUser
    template_name = 'members/applicant_list.jinja2'
    context_object_name = 'applicants'

    def get_queryset(self):
        queryset = ApplicantUser.objects.published().prefetch_related(
            'followers', '_skills', 'job_groups')
        return ApplicantUserFilter(self.request.GET, queryset=queryset).qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['choices_looking'] = ApplicantUser.CHOICES_LOOKING
        context['choices_type'] = ApplicantUser.CHOICES_TYPE
        return context


class ApplicantUpdateView(TemplateView):
    template_name = 'members/applicant_update.jinja2'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ApplicantDetailView(DetailView):
    model = ApplicantUser
    queryset = ApplicantUser.objects.prefetch_related(
        'skills__skill',
        'links__link',
    )
    template_name = 'members/applicant_detail.jinja2'
    context_object_name = 'applicant'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['choices_level'] = ApplicantSkill.CHOICES_LEVEL
        return context


class LoginView(DjangoLoginView):
    form_class = LoginForm
    template_name = 'members/login.jinja2'


class LogoutView(DjangoLogoutView):
    pass


class SignupView(TemplateView):
    template_name = 'members/signup.jinja2'


class ApplicantSignupView(StaticContentMixin, FormView):
    form_class = ApplicantSignupForm
    template_name = 'members/signup_applicant.jinja2'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class CompanySignupView(StaticContentMixin, FormView):
    form_class = CompanySignupForm
    template_name = 'members/signup_company.jinja2'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
