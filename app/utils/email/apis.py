from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from members.permissions import IsCompanyUser
from utils.email.serializers import HireEmailSendSerializer

__all__ = (
    'HireEmailSendAPIView',
)


class HireEmailSendAPIView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
        IsCompanyUser,
    )

    def post(self, request):
        serializer = HireEmailSendSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            result = serializer.send()
            return Response(result, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
