import textwrap

from django.conf import settings
from django.db import models

from .user import User, UserManager

__all__ = (
    'ApplicantUser',
    'Link',
    'ApplicantLink',
    'Skill',
    'ApplicantSkill',
    'Education',
    'Career',
    'License',
)


class ApplicantUserManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(type=User.TYPE_APPLICANT)


class ApplicantUser(User):
    objects = ApplicantUserManager()

    class Meta:
        proxy = True
        verbose_name = '지원자'
        verbose_name_plural = f'{verbose_name} 목록'

    def __str__(self):
        return self.name


class Link(models.Model):
    title = models.CharField('링크타입명', max_length=50)
    img_icon = models.ImageField('아이콘', upload_to='link', blank=True)

    class Meta:
        verbose_name = '프로필 링크 아이템'
        verbose_name_plural = f'{verbose_name} 목록'

    def __str__(self):
        return self.title


class ApplicantLink(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='links', related_query_name='link')
    link = models.ForeignKey(Link, on_delete=models.CASCADE, related_name='+')
    url = models.URLField('주소')

    def __str__(self):
        return '{user} - {link} ({url})'.format(
            user=self.user.name,
            link=self.link.title,
            url=textwrap.shorten(self.url, width=15, placeholder='...'),
        )

    @property
    def title(self):
        return self.link.title

    @property
    def img_icon(self):
        return self.link.img_icon


class Skill(models.Model):
    title = models.CharField('기술명', max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '보유기술'
        verbose_name_plural = f'{verbose_name} 목록'


class ApplicantSkill(models.Model):
    CHOICES_LEVEL = (
        ('high', '매우능숙'),
        ('mid', '능숙'),
        ('low', '활용가능'),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='skills', related_query_name='skill')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='+')
    level = models.CharField('숙련도', max_length=5, choices=CHOICES_LEVEL)

    def __str__(self):
        return '{user} - {skill} ({level})'.format(
            user=self.user.name,
            skill=self.skill.title,
            level=self.get_level_display(),
        )

    @property
    def title(self):
        return self.skill.title


class Education(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='지원자', on_delete=models.CASCADE)
    start_date = models.DateField('시작일자')
    end_date = models.DateField('종료일자', blank=True, null=True)
    content = models.TextField('내역')

    def __str__(self):
        return '{content} ({start_date}{end_date})'.format(
            content=textwrap.shorten(self.content, width=14, placeholder='...'),
            start_date=self.start_date,
            end_date=self.end_date,
        )


class Career(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='지원자', on_delete=models.CASCADE)
    start_date = models.DateField('시작일자')
    end_date = models.DateField('종료일자', blank=True, null=True)
    content = models.TextField('내역')

    def __str__(self):
        return '{content} ({start_date}{end_date})'.format(
            content=textwrap.shorten(self.content, width=14, placeholder='...'),
            start_date=self.start_date,
            end_date=self.end_date,
        )


class License(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='지원자', on_delete=models.CASCADE)
    get_date = models.DateField('취득일자')
    organization = models.CharField('발급기관', max_length=100)
    title = models.CharField('이름', max_length=100)

    def __str__(self):
        return f'{self.organization} - {self.title} ({self.get_date})'
