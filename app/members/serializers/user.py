from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from ..models import UserLike

__all__ = (
    'UserLikeCreateSerializer',
)


class UserLikeCreateSerializer(serializers.ModelSerializer):
    from_user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = UserLike
        fields = (
            'from_user',
            'to_user',
        )
        read_only_fields = (
            'from_user',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=UserLike.objects.all(),
                fields=('from_user', 'to_user'),
            )
        ]
