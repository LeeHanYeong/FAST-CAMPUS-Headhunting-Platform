from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from administrator.models import MailingGroup
from .user import User, UserManager

__all__ = (
    'CompanyUser',
)


class CompanyUserAdmin(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(type=User.TYPE_COMPANY)


class CompanyUser(User):
    objects = CompanyUserAdmin()

    class Meta:
        proxy = True
        verbose_name = '기업회원'
        verbose_name_plural = f'{verbose_name} 목록'

    def save(self, *args, **kwargs):
        self.type = User.TYPE_COMPANY
        self.is_active = True
        super().save(*args, **kwargs)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    @property
    def hire_job_groups(self):
        return self._hire_job_groups

    @hire_job_groups.setter
    def hire_job_groups(self, value):
        self._hire_job_groups = value

    def send_company_user_signup_notification(self):
        html_content = render_to_string(
            'email/company_user_add_hire_job_group.jinja2', {
                'user': self,
                'site': Site.objects.get_current(),
            }
        )
        text_content = strip_tags(html_content)
        message = EmailMultiAlternatives(
            subject='기업회원 채용희망직군 추가 안내',
            body=text_content,
            from_email=settings.EMAIL_HOST_USER,
            to=list(MailingGroup.objects.get(
                code=MailingGroup.CODE_COMPANY_USER_JOBGROUP_APPROVE
            ).users.values_list('email', flat=True)),
        )
        message.attach_alternative(html_content, 'text/html')
        result = message.send()
        return result
