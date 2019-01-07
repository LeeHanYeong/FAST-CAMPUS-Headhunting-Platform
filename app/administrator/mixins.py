from django.views.generic.base import ContextMixin

from .models import StaticContent

__all__ = (
    'StaticContentMixin',
)


class StaticContentMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        static_content = StaticContent.objects.first()
        if not StaticContent.objects.exists():
            static_content = StaticContent.objects.create()
        context['static_content'] = static_content
        return context
