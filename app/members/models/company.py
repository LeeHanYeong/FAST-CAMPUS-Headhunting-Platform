from .user import User, UserManager

__all__ = (
    'CompanyUser',
)


class CompanyUserAdmin(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(type=User.TYPE_COMPANY)


class CompanyUser(User):
    objects = CompanyUserAdmin()

    class Meta:
        proxy = True
        verbose_name = '기업회원'
        verbose_name_plural = f'{verbose_name} 목록'

    def __str__(self):
        return f'{self._company_name} - {self.name} ({self._position})'

    def save(self, *args, **kwargs):
        self.type = User.TYPE_COMPANY
        super().save(*args, **kwargs)

    @property
    def company_name(self):
        return self._company_name

    @property
    def position(self):
        return self._position
