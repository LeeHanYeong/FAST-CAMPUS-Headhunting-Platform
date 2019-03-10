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

    def save(self, *args, **kwargs):
        self.type = User.TYPE_COMPANY
        self.is_active = True
        super().save(*args, **kwargs)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    @property
    def hire_job_groups(self):
        return self._hire_job_groups

    @hire_job_groups.setter
    def hire_job_groups(self, value):
        self._hire_job_groups = value
