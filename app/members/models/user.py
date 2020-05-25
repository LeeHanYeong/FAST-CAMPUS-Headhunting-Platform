from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.db.models.functions import Concat
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags
from django_fields import DefaultStaticImageField
from phonenumber_field.modelfields import PhoneNumberField

from administrator.models import Company
from utils.models import TimeStampedMixin

__all__ = (
    'UserManager',
    'User',
    'UserLike',
    'CompanyUserHireJobGroupWithApprovalStatus',
)


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('이메일은 필수항목입니다')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('type', User.TYPE_STAFF)
        extra_fields.setdefault('birth_date', timezone.now()),

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(TimeStampedMixin, AbstractUser):
    TYPE_STAFF = 's'
    TYPE_APPLICANT = 'a'
    TYPE_COMPANY = 'c'
    CHOICES_TYPE = (
        (TYPE_APPLICANT, '지원자'),
        (TYPE_COMPANY, '채용연계기업'),
        (TYPE_STAFF, '관리자'),
    )

    LOOKING_NEW = 'n'
    LOOKING_EXP = 'e'
    LOOKING_SWITCHING = 's'
    LOOKING_COMPLETE = 'c'
    CHOICES_LOOKING = (
        (LOOKING_NEW, '신입'),
        (LOOKING_EXP, '경력'),
        (LOOKING_SWITCHING, '커리어 전환'),
    )
    username = None
    is_active = models.BooleanField('활성화 여부', default=False)
    last_name = models.CharField('성', max_length=150)
    first_name = models.CharField('이름', max_length=30)
    type = models.CharField('타입', max_length=1, choices=CHOICES_TYPE, default=TYPE_STAFF)
    email = models.EmailField('이메일', unique=True)
    phone_number = PhoneNumberField('전화번호', blank=True)
    like_users = models.ManyToManyField(
        'self', symmetrical=False, through='UserLike',
        verbose_name='즐겨찾기 한 유저 목록', related_name='followers', blank=True)

    # 기업회원 필드
    _company = models.ForeignKey(
        Company, on_delete=models.CASCADE, verbose_name='회사',
        blank=True, null=True, related_name='users')
    _company_name = models.CharField('회사명', max_length=80, blank=True)
    _position = models.CharField('직책', max_length=50, blank=True)
    _hire_job_groups = models.ManyToManyField(
        'courses.JobGroup', verbose_name='채용희망직군',
        through='CompanyUserHireJobGroupWithApprovalStatus', blank=True,
        related_name='hire_company_user_set', related_query_name='hire_company_user',
    )

    # 지원자 필드
    is_published = models.BooleanField('이력서 공개여부', default=False)
    is_looking = models.CharField(
        '지원자 상태', choices=CHOICES_LOOKING, default=LOOKING_SWITCHING, max_length=1)
    img_profile = DefaultStaticImageField(
        '프로필 이미지', upload_to='user', blank=True,
        default_image_path='images/blank_user.png',
    )
    birth_date = models.DateField('생년월일', blank=True, null=True)
    short_intro = models.CharField('한 줄 소개', max_length=200, blank=True)
    introduce = RichTextUploadingField('소개', blank=True)

    pdf1 = models.FileField('PDF1', upload_to='users/pdf', blank=True)
    pdf2 = models.FileField('PDF2', upload_to='users/pdf', blank=True)
    _links = models.ManyToManyField(
        'Link', verbose_name='링크 목록', blank=True,
        through='ApplicantLink', related_name='users', related_query_name='user',
    )
    _skills = models.ManyToManyField(
        'Skill', verbose_name='보유 기술 목록', blank=True,
        through='ApplicantSkill', related_name='users', related_query_name='user',
    )
    job_groups = models.ManyToManyField(
        'courses.JobGroup', verbose_name='취업희망 직군 목록', blank=True,
        related_name='users', related_query_name='user',
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['-pk']
        verbose_name = '사용자'
        verbose_name_plural = f'{verbose_name} 목록'

    def __str__(self):
        if self.type == self.TYPE_STAFF:
            return f'[관리자] {self.name} ({self.email})'
        elif self.type == self.TYPE_COMPANY:
            return f'[기업회원] {self.name} ({self.email}) | {self.company_info} '
        elif self.type == self.TYPE_APPLICANT:
            return f'[지원자] {self.name}'
        return self.name

    @property
    def name(self):
        return f'{self.last_name}{self.first_name}'

    @property
    def company_name(self):
        if self._company:
            return self._company.name
        return self._company_name

    @property
    def company_info(self):
        return f'{self.company_name} ({self._position})'

    name.fget.short_description = '이름'
    name.fget.admin_order_field = Concat('last_name', 'first_name')

    def send_signup_approve(self):
        html_content = render_to_string(
            'email/signup_confirm.jinja2', {
                'user': self,
                'site': Site.objects.get_current(),
            }
        )
        text_content = strip_tags(html_content)
        message = EmailMultiAlternatives(
            subject='이용 승인 안내',
            body=text_content,
            from_email=settings.EMAIL_HOST_USER,
            to=[self.email],
        )
        message.attach_alternative(html_content, 'text/html')
        result = message.send()
        return result


class UserLike(TimeStampedMixin, models.Model):
    from_user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='from_user_userlike_set',
    )
    to_user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='to_user_userlike_set',
    )

    class Meta:
        verbose_name = '사용자 찜'
        verbose_name_plural = f'{verbose_name} 목록'
        unique_together = (
            ('from_user', 'to_user'),
        )


class CompanyUserHireJobGroupWithApprovalStatusManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).prefetch_related(
            'job_group__category',
        ).select_related(
            'company_user___company',
        )


class CompanyUserHireJobGroupWithApprovalStatus(models.Model):
    """
    기업회원이 채용을 원하는 직군과의 M2M연결 중간모델
    """
    STATUS_WAIT, STATUS_APPROVAL = ('wait', 'approval')
    CHOICES_STATUS = (
        (STATUS_WAIT, '승인대기중'),
        (STATUS_APPROVAL, '승인완료'),
    )
    company_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='기업회원', on_delete=models.CASCADE,
        related_name='hire_job_group_set', related_query_name='hire_job_group',
    )
    job_group = models.ForeignKey(
        'courses.JobGroup', verbose_name='직군', on_delete=models.CASCADE,
        related_name='hire_job_group_set', related_query_name='hire_job_group',
    )
    status = models.CharField('승인상태', choices=CHOICES_STATUS, max_length=20, default=STATUS_WAIT)

    objects = CompanyUserHireJobGroupWithApprovalStatusManager()

    class Meta:
        verbose_name = '기업회원의 채용희망직군 관리자 승인'
        verbose_name_plural = f'{verbose_name} 목록'
        unique_together = (
            ('company_user', 'job_group'),
        )

    def __str__(self):
        return '{user} | {job_group} [{status}]'.format(
            user=self.company_user.name,
            job_group=self.job_group.title,
            status=self.get_status_display(),
        )
