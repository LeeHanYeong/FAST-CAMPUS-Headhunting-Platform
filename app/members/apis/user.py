from rest_framework import generics, permissions

from ..models import UserLike
from ..serializers import UserLikeCreateSerializer

__all__ = (
    'UserLikeCreateAPIView',
)


class UserLikeCreateAPIView(generics.CreateAPIView):
    queryset = UserLike.objects.all()
    serializer_class = UserLikeCreateSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user)
