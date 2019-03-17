from urllib import request

import boto3
from django.conf import settings
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        ip = request.urlopen('http://ifconfig.me/ip').read().decode('utf-8')
        session = boto3.session.Session(
            profile_name=settings.AWS_EB_SESSION_PROFILE,
            region_name='ap-northeast-2',
        )
        ec2 = session.resource('ec2')
        sg_rds = ec2.SecurityGroup(settings.AWS_RDS_SECURITY_GROUP_ID)
        exist_permissions = sg_rds.ip_permissions
        if exist_permissions:
            sg_rds.revoke_ingress(IpPermissions=exist_permissions)
        sg_rds.authorize_ingress(
            IpPermissions=[{
                'FromPort': settings.DATABASES['default']['PORT'],
                'ToPort': settings.DATABASES['default']['PORT'],
                'IpProtocol': 'TCP',
                'IpRanges': [{
                    'CidrIp': f'{ip}/32',
                }],
                'UserIdGroupPairs': [{
                    'GroupId': settings.AWS_EB_ENVIRONMENTS_SECURITY_GROUP_ID,
                    'UserId': settings.AWS_EB_USER_ID,
                }],
            }],
        )
