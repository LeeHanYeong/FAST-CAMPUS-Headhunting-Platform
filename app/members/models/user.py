from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django_fields import DefaultStaticImageField
from phonenumber_field.modelfields import PhoneNumberField

from utils.models import TimeStampedMixin

__all__ = (
    'UserManager',
    'User',
    'UserLike',
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


class User(TimeStampedMixin, AbstractUser):
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
    like_users = models.ManyToManyField(
        'self', symmetrical=False, through='UserLike',
        verbose_name='즐겨찾기 한 유저 목록', related_name='followers', blank=True)

    # 기업회원 필드
    _company_name = models.CharField('회사명', max_length=80, blank=True)
    _position = models.CharField('직책', max_length=50, blank=True)

    # 지원자 필드
    is_published = models.BooleanField('이력서 공개여부', default=False)
    is_looking = models.BooleanField('구직 여부', default=True)
    img_profile = DefaultStaticImageField(
        '프로필 이미지', upload_to='user', blank=True,
        default_image_path='images/blank_user.png',
    )
    birth_date = models.DateField('생년월일', blank=True, null=True)
    short_intro = models.CharField('한 줄 소개', max_length=200, blank=True)
    introduce = RichTextUploadingField('소개', blank=True)

    _links = models.ManyToManyField(
        'Link', verbose_name='링크 목록', blank=True,
        through='ApplicantLink', related_name='users', related_query_name='user',
    )
    _skills = models.ManyToManyField(
        'Skill', verbose_name='보유 기술 목록', blank=True,
        through='ApplicantSkill', related_name='users', related_query_name='user',
    )

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
        unique_together = (
            ('from_user', 'to_user'),
        )
