from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.views import (
    LogoutView as DjangoLogoutView,
    LoginView as DjangoLoginView,
    PasswordChangeView as DjangoPasswordChangeView,
    PasswordChangeDoneView as DjangoPasswordChangeDoneView,
    PasswordResetView as DjangoPasswordResetView,
    PasswordResetConfirmView as DjangoPasswordResetConfirmView,
    PasswordResetDoneView as DjangoPasswordResetDoneView,
    PasswordResetCompleteView as DjangoPasswordResetCompleteView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import F, Exists, OuterRef
from django.db.models.functions import Concat
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, FormView, DetailView

from administrator.mixins import StaticContentMixin
from courses.models import JobCategory, JobGroup
from .filters import ApplicantUserFilter
from .forms import LoginForm, ApplicantSignupForm, CompanySignupForm, PasswordResetForm, SetPasswordForm, \
    PasswordChangeForm
from .models import ApplicantUser, ApplicantSkill, CompanyUserHireJobGroupWithApprovalStatus

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


class ApplicantUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'members/applicant_update.jinja2'


class ApplicantDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
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
        user = self.request.user
        applicant = self.get_object()
        if user.type == User.TYPE_STAFF:
            return True
        elif user.type == User.TYPE_APPLICANT:
            return user == applicant
        elif user.type == User.TYPE_COMPANY:
            return user.hire_job_group_set.filter(
                job_group__in=applicant.job_groups.all(),
                status=CompanyUserHireJobGroupWithApprovalStatus.STATUS_APPROVAL,
            ).exists()


class ApplicantProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'members/applicant_profile.jinja2'


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


class CompanyUserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'members/company_profile.jinja2'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 승인여부를 QuerySet에 포함
        wait_hire_job_groups = CompanyUserHireJobGroupWithApprovalStatus.objects.filter(
            job_group=OuterRef('pk'),
            company_user=self.request.user,
            status=CompanyUserHireJobGroupWithApprovalStatus.STATUS_WAIT
        )
        approval_hire_job_groups = CompanyUserHireJobGroupWithApprovalStatus.objects.filter(
            job_group=OuterRef('pk'),
            company_user=self.request.user,
            status=CompanyUserHireJobGroupWithApprovalStatus.STATUS_APPROVAL
        )
        context['job_category_set'] = JobCategory.objects.prefetch_related('group_set')
        context['subquery_set'] = {
            'wait': wait_hire_job_groups,
            'approval': approval_hire_job_groups,
            'Exists': Exists,
        }
        return context


class CompanyUserHireJobGroupAddRequestView(LoginRequiredMixin, View):
    def post(self, request):
        job_group_pk_list = request.POST.getlist('job_group')
        for job_group_pk in job_group_pk_list:
            self.request.user.hire_job_group_set.create(job_group=JobGroup.objects.get(pk=job_group_pk))
        return redirect('members:company-user-profile')


class PasswordChangeView(DjangoPasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'members/password_change_form.jinja2'
    success_url = reverse_lazy('members:password-change-done')


class PasswordChangeDoneView(DjangoPasswordChangeDoneView):
    template_name = 'members/password_change_done.jinja2'


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
    success_url = reverse_lazy('members:password-reset-complete')


class PasswordResetCompleteView(DjangoPasswordResetCompleteView):
    template_name = 'members/password_reset_complete.jinja2'
