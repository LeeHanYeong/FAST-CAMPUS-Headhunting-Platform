from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin, PermissionRequiredMixin
from django.views import View

User = get_user_model()

__all__ = (
    'CompanyUserMixin',
)


class CompanyUserMixin(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.type == User.TYPE_COMPANY
