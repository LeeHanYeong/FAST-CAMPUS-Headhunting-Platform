from rest_framework import generics

from .models import JobCategory
from .serializers import JobCategorySerializer


class JobCategoryListAPIView(generics.ListAPIView):
    queryset = JobCategory.objects.prefetch_related('group_set')
    serializer_class = JobCategorySerializer
