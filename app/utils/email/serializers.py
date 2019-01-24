from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from members.models import ApplicantUser
from members.serializers import ApplicantUserSerializer, UserSerializer
from utils.email.case.hire import send_hire_mail

__all__ = (
    'HireEmailSendSerializer',
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


class HireEmailSendSerializer(serializers.Serializer):
    subject = serializers.CharField(required=True)
    message = serializers.CharField(required=True)
    company_user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    applicant = serializers.IntegerField()

    def validate_applicant(self, value):
        applicant = get_object_or_404(ApplicantUser, pk=value)
        return applicant

    def send(self):
        result_applicant, result_company = send_hire_mail(**self.validated_data)
        if not result_applicant:
            raise HireEmailSendException(
                recipient=self.validated_data['applicant'],
                subject=self.validated_data['subject'],
                message=self.validated_data['message'],
            )
        elif not result_company:
            raise HireEmailSendException(
                recipient=self.validated_data['company_user'],
                subject=self.validated_data['subject'],
                message=self.validated_data['message'],
            )
        data = {
            'applicant': ApplicantUserSerializer(self.validated_data['applicant']).data,
            'company_user': UserSerializer(self.validated_data['company_user']).data,
        }
        return data
