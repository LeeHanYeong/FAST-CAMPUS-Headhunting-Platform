from django.conf import settings
from django.core.mail import send_mail

from administrator.models import MailingGroup

EMAIL_SUBJECT_APPLICANT = '채용연계기업 매칭 알림'
EMAIL_CONTENT_APPLICANT = '''{applicant_name}님, 패스트캠퍼스입니다.

채용연계기업 매칭이 되었음을 알려드립니다.
아래의 정보를 확인하신 후 담당자님께 꼭 답장 해주세요.

보내는 사람: {company_user_name} ({company_user_email})

제목: {subject}

본문
{message}
'''

EMAIL_SUBJECT_COMPANY = '채용연계메일 발송 알림'
EMAIL_CONTENT_COMPANY = '''{company_user_name}님, 안녕하세요. 패스트캠퍼스입니다.

담당자님께서 보내주신 메일이 지원자({applicant_name})에게 잘 전달되었습니다.
기업이 추구하는 방향에 맞는 훌륭한 인재를 찾으시길 바랍니다. :)

감사합니다.
패스트캠퍼스 드림.
'''

EMAIL_SUBJECT_STAFF = '채용연계메일 발송 알림'
EMAIL_CONTENT_STAFF = '''{company_user_name}으로부터 {applicant_name}으로 메일 발송

보내는 사람: {company_user_name} ({company_user_email})

제목: {subject}

본문
{message}
'''

__all__ = (
    'send_hire_mail',
)


class HireEmailSendException(Exception):
    def __init__(self, recipient, subject, message):
        self.recipient = recipient
        self.subject = subject
        self.message = message

    def __str__(self):
        return '채용매칭 메일 발송 오류 (수신: {recipient}, 제목: {subject}, 내용: {message}'.format(
            recipient=f'{self.recipient.name} ({self.recipient.email})',
            subject=self.subject,
            message=self.message,
        )


def send_hire_mail(company_user, applicant, subject, message):
    # 지원자에게 전송
    result_applicant = send_mail(
        subject=EMAIL_SUBJECT_APPLICANT,
        message=EMAIL_CONTENT_APPLICANT.format(
            applicant_name=applicant.name,
            company_user_name=company_user.name,
            company_user_email=company_user.email,
            subject=subject,
            message=message,
        ),
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[applicant.email],
    )

    # 기업회원에게 전송
    result_company = send_mail(
        subject=EMAIL_SUBJECT_COMPANY,
        message=EMAIL_CONTENT_COMPANY.format(
            company_user_name=company_user.name,
            applicant_name=applicant.name,
        ),
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[company_user.email],
    )

    if not result_applicant:
        raise HireEmailSendException(
            recipient=applicant,
            subject=subject,
            message=message,
        )

    if not result_company:
        raise HireEmailSendException(
            recipient=company_user,
            subject=subject,
            message=message,
        )

    # 관리자에게 전송
    staff_list = MailingGroup.objects.get(code=MailingGroup.CODE_SEND_HIRE_MAIL).users.all()
    if staff_list.exists():
        result_staff = send_mail(
            subject=EMAIL_SUBJECT_STAFF,
            message=EMAIL_CONTENT_STAFF.format(
                applicant_name=applicant.name,
                company_user_name=company_user.name,
                company_user_email=company_user.email,
                subject=subject,
                message=message,
            ),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=list(staff_list.values_list('email', flat=True)),
        )
