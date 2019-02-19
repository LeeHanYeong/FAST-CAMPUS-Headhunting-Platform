from django.test import TestCase
from model_mommy import mommy

from courses.models import JobGroup
from .forms import ApplicantSignupForm, CompanySignupForm


class SignupTest(TestCase):
    APPLICANT_EMAIL = 'me@lhy.kr'
    APPLICANT_LAST_NAME = '박'
    APPLICANT_FIRST_NAME = '보영'
    APPLICANT_PASSWORD = 'dlgksdud'
    APPLICANT_PHONE_NUMBER = '010-4432-1234'

    COMPANY_EMAIL = 'dev@lhy.kr'
    COMPANY_LAST_NAME = '아'
    COMPANY_FIRST_NAME = '이유'
    COMPANY_PASSWORD = 'dlgksdud'
    COMPANY_PHONE_NUMBER = '010-1234-1234'

    def test_applicant_signup_form(self):
        data = {
            'email': self.APPLICANT_EMAIL,
            'last_name': self.APPLICANT_LAST_NAME,
            'first_name': self.APPLICANT_FIRST_NAME,
            'password1': self.APPLICANT_PASSWORD,
            'password2': self.APPLICANT_PASSWORD,
            'phone_number': self.APPLICANT_PHONE_NUMBER,
        }
        form = ApplicantSignupForm(data=data)
        form_valid = form.is_valid()
        self.assertTrue(form_valid)
        user = form.save()
        self.assertEqual(user.email, self.APPLICANT_EMAIL)

    def test_company_user_signup_form(self):
        job_group = mommy.make(JobGroup)
        data = {
            'email': self.COMPANY_EMAIL,
            'last_name': self.COMPANY_LAST_NAME,
            'first_name': self.COMPANY_FIRST_NAME,
            'password1': self.COMPANY_PASSWORD,
            'password2': self.COMPANY_PASSWORD,
            'phone_number': self.COMPANY_PHONE_NUMBER,
            '_position': '대리',
            '_company_name': '패스트캠퍼스',
            'hire_job_groups': [job_group.pk],
        }
        form = CompanySignupForm(data=data)
        form_valid = form.is_valid()
        self.assertTrue(form_valid)
        user = form.save()
        self.assertEqual(user.email, self.COMPANY_EMAIL)
