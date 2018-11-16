from rest_framework import generics, permissions, mixins
from rest_framework.generics import get_object_or_404

from ..models import UserLike
from ..permissions import IsFromUser
from ..serializers import UserLikeCreateDeleteSerializer

__all__ = (
    'UserLikeCreateDestoryAPIView',
)


class UserLikeCreateDestoryAPIView(mixins.DestroyModelMixin, generics.CreateAPIView):
    queryset = UserLike.objects.all()
    serializer_class = UserLikeCreateDeleteSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsFromUser,
    )

    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user)

    def get_object(self):
        return get_object_or_404(
            UserLike,
            from_user=self.request.user,
            to_user=self.request.data.get('to_user'),
        )

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
