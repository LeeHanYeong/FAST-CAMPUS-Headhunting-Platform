from ckeditor.fields import RichTextField
from colorful.fields import RGBColorField
from django.db import models
from django_extensions.db.models import TimeStampedModel
from django_fields import DefaultStaticImageField


class StaticContent(models.Model):
    index_image = models.ImageField(
        '메인페이지 이미지', upload_to='index', blank=True)
    index_color = RGBColorField(
        '메인페이지 배경색', help_text='배너 이미지의 남는 공간을 채울 배경색입니다.', blank=True)
    index_height = models.IntegerField(
        '메인페이지 이미지 세로 길이(px)', default=200,
        help_text='메인 배너 이미지의 세로 길이를 지정합니다. 가로길이는 세로 길이의 비율로 정해집니다.')

    index_mobile_image = models.ImageField(
        '메인페이지 모바일 이미지', help_text='모바일 이미지는 가로를 가득 채우도록 설정됩니다',
        upload_to='index', blank=True)
    index_mobile_color = RGBColorField('메인페이지 모바일 배경색', blank=True)

    company_list_image = models.ImageField(
        '참여기업 목록 이미지', help_text='참여기업 목록의 배너 이미지 입니다.', upload_to='static', blank=True)

    privacy_policy = RichTextField('개인정보 취급방침', blank=True)
    terms_of_service = RichTextField('이용약관', blank=True)

    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '정적 콘텐츠'
        verbose_name_plural = f'{verbose_name} 목록'

    def __str__(self):
        return f'정적 콘텐츠 (수정: {self.modified})'


class Service(models.Model):
    title = models.CharField('서비스명', max_length=30)

    class Meta:
        verbose_name = '기업 서비스 분류'
        verbose_name_plural = f'{verbose_name} 목록'

    def __str__(self):
        return self.title


class Company(TimeStampedModel):
    TYPE_STARTUP = 's'
    TYPE_AGENCY = 'a'
    TYPE_NORMAL = 'n'
    CHOICES_TYPE = (
        (TYPE_STARTUP, '스타트업'),
        (TYPE_AGENCY, '에이전시'),
        (TYPE_NORMAL, '일반기업'),
    )
    type = models.CharField('기업 종류', choices=CHOICES_TYPE, max_length=1)
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE,
        verbose_name='서비스 종류', blank=True, null=True)
    name = models.CharField('회사명', max_length=100, db_index=True)
    img_logo = DefaultStaticImageField(
        '로고', upload_to='company', blank=True, default_image_path='blank_user.png')
    url = models.URLField('URL', blank=True)
    is_show = models.BooleanField('참여기업 목록에 표시', default=False)

    class Meta:
        ordering = ['name']
        verbose_name = '회사'
        verbose_name_plural = f'{verbose_name} 목록'

    def __str__(self):
        return self.name
