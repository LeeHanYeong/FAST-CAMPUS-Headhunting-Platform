from ckeditor.fields import RichTextField
from colorful.fields import RGBColorField
from django.db import models
from django_extensions.db.models import TimeStampedModel


class StaticContent(models.Model):
    index_image = models.ImageField('메인페이지 이미지', upload_to='index', blank=True)
    index_color = RGBColorField('메인페이지 배경색', blank=True)
    privacy_policy = RichTextField('개인정보 취급방침', blank=True)
    terms_of_service = RichTextField('이용약관', blank=True)

    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '정적 콘텐츠'
        verbose_name_plural = f'{verbose_name} 목록'

    def __str__(self):
        return f'정적 콘텐츠 (수정: {self.modified})'


class Company(TimeStampedModel):
    name = models.CharField('회사명', max_length=100, db_index=True)
    img_logo = models.ImageField('로고', upload_to='company', blank=True)
    is_show = models.BooleanField('참여기업 목록에 표시', default=False)

    class Meta:
        ordering = ['name']
        verbose_name = '회사'
        verbose_name_plural = f'{verbose_name} 목록'

    def __str__(self):
        return self.name
