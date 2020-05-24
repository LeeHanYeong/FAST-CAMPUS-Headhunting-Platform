from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from members.models import ApplicantUser
from members.serializers import ApplicantUserSerializer, UserSerializer
from utils.email.case.hire import send_hire_mail

__all__ = (
    'HireEmailSendSerializer',
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
        send_hire_mail(**self.validated_data)

        data = {
            'applicant': ApplicantUserSerializer(self.validated_data['applicant']).data,
            'company_user': UserSerializer(self.validated_data['company_user']).data,
        }
        return data
