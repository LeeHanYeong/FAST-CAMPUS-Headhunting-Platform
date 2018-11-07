from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

__all__ = (
    'UserManager',
    'User',
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
        extra_fields.setdefault('type', User.TYPE_STAFF)
        extra_fields.setdefault('birth_date', timezone.now()),

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    TYPE_STAFF = 's'
    TYPE_APPLICANT = 'a'
    TYPE_COMPANY = 'c'
    CHOICES_TYPE = (
        (TYPE_APPLICANT, '지원자'),
        (TYPE_COMPANY, '참여기업'),
    )
    username = None
    last_name = models.CharField('성', max_length=150)
    first_name = models.CharField('이름', max_length=30)
    type = models.CharField('타입', max_length=1, choices=CHOICES_TYPE, default=TYPE_STAFF)
    email = models.EmailField('이메일', unique=True)
    phone_number = PhoneNumberField('전화번호', blank=True)
    # 지원자 필드
    birth_date = models.DateField('생년월일', blank=True, null=True)
    introduce = models.TextField('소개', blank=True)

    _links = models.ManyToManyField(
        'Link', verbose_name='링크 목록', blank=True,
        through='ApplicantLink', related_name='users', related_query_name='user',
    )
    _skills = models.ManyToManyField(
        'Skill', verbose_name='보유 기술 목록', blank=True,
        through='ApplicantSkill', related_name='users', related_query_name='user',
    )

    # 기업회원 필드
    _company_name = models.CharField('회사명', max_length=80, blank=True)
    _position = models.CharField('직책', max_length=50, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['-pk']
        verbose_name = '사용자'
        verbose_name_plural = f'{verbose_name} 목록'

    @property
    def name(self):
        return f'{self.last_name}{self.first_name}'

    name.fget.short_description = '이름'