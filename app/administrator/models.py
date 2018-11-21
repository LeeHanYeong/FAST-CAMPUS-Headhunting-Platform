from ckeditor.fields import RichTextField
from django.db import models


class StaticContent(models.Model):
    privacy_policy = RichTextField('개인정보 취급방침', blank=True)
    terms_of_service = RichTextField('이용약관', blank=True)

    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '정적 콘텐츠'
        verbose_name_plural = f'{verbose_name} 목록'

    def __str__(self):
        return f'정적 콘텐츠 (수정: {self.modified_at})'
