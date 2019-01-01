from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from ..models import UserLike

User = get_user_model()

__all__ = (
    'UserLikeCreateDeleteSerializer',
    'UserSerializer',
)


class UserLikeCreateDeleteSerializer(serializers.ModelSerializer):
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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'first_name',
            'last_name',
            'email',
        )
