from django.contrib.auth import login, get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.views import (
    LogoutView as DjangoLogoutView,
    LoginView as DjangoLoginView,
    PasswordResetView as DjangoPasswordResetView,
    PasswordResetConfirmView as DjangoPasswordResetConfirmView,
    PasswordResetDoneView as DjangoPasswordResetDoneView,
    PasswordResetCompleteView as DjangoPasswordResetCompleteView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import F
from django.db.models.functions import Concat
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, FormView, DetailView

from administrator.mixins import StaticContentMixin
from courses.models import JobCategory
from .filters import ApplicantUserFilter
from .forms import LoginForm, ApplicantSignupForm, CompanySignupForm, PasswordResetForm, SetPasswordForm
from .models import ApplicantUser, ApplicantSkill

User = get_user_model()


class ApplicantListView(LoginRequiredMixin, ListView):
    model = ApplicantUser
    template_name = 'members/applicant_list.jinja2'
    context_object_name = 'applicants'

    def get_queryset(self):
        queryset = ApplicantUser.objects.published() \
            .prefetch_related('followers', '_skills', 'job_groups', 'job_groups__category') \
            .annotate(full_name=Concat(F('last_name'), F('first_name')))
        return ApplicantUserFilter(self.request.GET, queryset=queryset).qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['choices_looking'] = ApplicantUser.CHOICES_LOOKING
        context['choices_type'] = ApplicantUser.CHOICES_TYPE
        try:
            category = JobCategory.objects.get(pk=self.request.GET.get('category'))
            context['cur_category'] = category
        except JobCategory.DoesNotExist:
            pass

        return context


class ApplicantUpdateView(TemplateView):
    template_name = 'members/applicant_update.jinja2'


class ApplicantDetailView(UserPassesTestMixin, DetailView):
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
        context['link_item_count'] = self.object.links.count()
        if self.object.pdf1:
            context['link_item_count'] += 1
        if self.object.pdf2:
            context['link_item_count'] += 1
        return context

    def test_func(self):
        return (self.request.user.type in (User.TYPE_COMPANY, User.TYPE_STAFF) or
                self.get_object() == self.request.user)


class LoginView(DjangoLoginView):
    form_class = LoginForm
    template_name = 'members/login.jinja2'


class LogoutView(DjangoLogoutView):
    pass


class SignupView(TemplateView):
    template_name = 'members/signup.jinja2'


class ApplicantSignupView(StaticContentMixin, SuccessMessageMixin, FormView):
    form_class = ApplicantSignupForm
    template_name = 'members/signup_applicant.jinja2'
    success_url = reverse_lazy('index')
    success_message = '회원가입이 완료되었습니다. 관리자의 승인 후 로그인 하실 수 있습니다'

    def form_valid(self, form):
        user = form.save()
        # login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return super().form_valid(form)


class CompanySignupView(StaticContentMixin, SuccessMessageMixin, FormView):
    form_class = CompanySignupForm
    template_name = 'members/signup_company.jinja2'
    success_url = reverse_lazy('index')
    success_message = '회원가입이 완료되었습니다. 관리자의 승인 후 로그인 하실 수 있습니다'

    def form_valid(self, form):
        user = form.save()
        return super().form_valid(form)


class PasswordResetView(DjangoPasswordResetView):
    email_template_name = 'members/password_reset_email.jinja2'
    form_class = PasswordResetForm
    subject_template_name = 'members/password_reset_subject.txt'
    success_url = reverse_lazy('members:password-reset-done')
    template_name = 'members/password_reset_form.jinja2'


class PasswordResetDoneView(DjangoPasswordResetDoneView):
    template_name = 'members/password_reset_done.jinja2'


class PasswordResetConfirmView(DjangoPasswordResetConfirmView):
    form_class = SetPasswordForm
    template_name = 'members/password_reset_confirm.jinja2'


class PasswordResetCompleteView(DjangoPasswordResetCompleteView):
    pass
