from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

EMAIL_SUBJECT = '기업회원 가입 안내'
EMAIL_CONTENT = '''
'''

__all__ = (
    'send_company_user_signup_notification',
)


def send_company_user_signup_notification(company_user):
    html_content = render_to_string(
        'email/company_user_signup_notification.jinja2', {
            'user': company_user,
            'site': Site.objects.get_current(),
        }
    )
    text_content = strip_tags(html_content)
    message = EmailMultiAlternatives(
        subject=EMAIL_SUBJECT,
        body=text_content,
        from_email=settings.EMAIL_HOST_USER,
        to=list(Group.objects.get(pk=1).user_set.values_list('email', flat=True)),
    )
    message.attach_alternative(html_content, 'text/html')
    result = message.send()
    return result
