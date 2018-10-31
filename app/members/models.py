from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = f'{verbose_name} 목록'
