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

    def published(self):
        return self.get_queryset().filter(is_published=True)


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
    EDU_TYPE_GRAD = 'grad'
    EDU_TYPE_GRAD_EX = 'grad_ex'
    EDU_TYPE_ATTEND = 'attend'
    EDU_TYPE_DROPOUT = 'dropout'
    CHOICES_EDU_TYPE = (
        (EDU_TYPE_GRAD, '졸업'),
        (EDU_TYPE_GRAD_EX, '졸업예정'),
        (EDU_TYPE_ATTEND, '재학'),
        (EDU_TYPE_DROPOUT, '중퇴'),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='지원자', on_delete=models.CASCADE)
    school = models.CharField('학교명', max_length=50)
    major = models.CharField('전공', max_length=50, blank=True)
    type = models.CharField('상태', choices=CHOICES_EDU_TYPE, max_length=12)
    start_date = models.DateField('시작일자')
    end_date = models.DateField('종료일자', blank=True, null=True)

    class Meta:
        verbose_name = '교육과정'
        verbose_name_plural = f'{verbose_name} 목록'

    def __str__(self):
        return '{school} ({start_date}{end_date})'.format(
            school=self.school,
            start_date=self.start_date,
            end_date=self.end_date,
        )


class Career(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='지원자', on_delete=models.CASCADE)
    organization = models.CharField('근무처', max_length=50)
    responsibility = models.CharField('담당 업무', max_length=50)
    position = models.CharField('직위', max_length=30)
    start_date = models.DateField('시작일자')
    end_date = models.DateField('종료일자', blank=True, null=True)
    content = models.TextField('내역')

    class Meta:
        verbose_name = '경력'
        verbose_name_plural = f'{verbose_name} 목록'

    def __str__(self):
        return '{organization} ({start_date}{end_date})'.format(
            organization=self.organization,
            start_date=self.start_date,
            end_date=self.end_date,
        )


class License(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='지원자', on_delete=models.CASCADE)
    title = models.CharField('자격증명', max_length=100)
    organization = models.CharField('발급기관', max_length=100)
    get_date = models.DateField('취득일자')

    class Meta:
        verbose_name = '자격증'
        verbose_name_plural = f'{verbose_name} 목록'

    def __str__(self):
        return f'{self.organization} - {self.title} ({self.get_date})'
