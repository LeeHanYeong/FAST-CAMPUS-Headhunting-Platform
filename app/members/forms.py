from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from courses.models import JobGroup
from .models import ApplicantUser, CompanyUser

ATTRS_FORM_CONTROL = {
    'class': 'form-control form-control-lg',
}


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        self.base_fields['username'].widget = forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
        })
        self.base_fields['password'].widget = forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
        })
        super().__init__(*args, **kwargs)


class ApplicantSignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        self.base_fields['password1'].widget = forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
        })
        self.base_fields['password2'].widget = forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
        })
        super().__init__(*args, **kwargs)

    class Meta:
        model = ApplicantUser
        fields = (
            'email',
            'last_name',
            'first_name',
            'password1',
            'password2',
            'phone_number',
        )
        widgets = {
            'email': forms.EmailInput(attrs=ATTRS_FORM_CONTROL),
            'last_name': forms.TextInput(attrs=ATTRS_FORM_CONTROL),
            'first_name': forms.TextInput(attrs=ATTRS_FORM_CONTROL),
            # 'phone_number': PhoneNumberPrefixWidget(attrs=ATTRS_FORM_CONTROL),
            'phone_number': forms.TextInput(attrs={
                'placeholder': '000-0000-0000',
                **ATTRS_FORM_CONTROL
            }),
        }


class CompanySignupForm(UserCreationForm):
    hire_job_groups = forms.ModelMultipleChoiceField(
        label='채용희망직군',
        queryset=JobGroup.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input',
        }),
    )

    def __init__(self, *args, **kwargs):
        self.base_fields['password1'].widget = forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
        })
        self.base_fields['password2'].widget = forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
        })
        super().__init__(*args, **kwargs)

    class Meta:
        model = CompanyUser
        fields = (
            'email',
            'last_name',
            'first_name',
            'password1',
            'password2',
            'phone_number',
            '_position',
            '_company',
            '_company_name',

            'hire_job_groups',
        )
        widgets = {
            'email': forms.EmailInput(attrs=ATTRS_FORM_CONTROL),
            'last_name': forms.TextInput(attrs=ATTRS_FORM_CONTROL),
            'first_name': forms.TextInput(attrs=ATTRS_FORM_CONTROL),
            'phone_number': forms.TextInput(attrs={
                'placeholder': '000-0000-0000',
                **ATTRS_FORM_CONTROL
            }),
            '_position': forms.TextInput(attrs=ATTRS_FORM_CONTROL),
            '_company': forms.Select(attrs={
                'v-model': 'company',
                **ATTRS_FORM_CONTROL
            }),
            '_company_name': forms.TextInput(attrs={
                'placeholder': '위의 목록에 회사명이 없을 경우 직접 입력해주세요',
                **ATTRS_FORM_CONTROL
            }),
        }

    def save(self, commit=True):
        instance = super().save(commit)
        hire_job_groups = self.cleaned_data['hire_job_groups']
        for job_group in hire_job_groups:
            instance.hire_job_group_set.create(job_group=job_group)
        return instance
