from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()

__all__ = (
    'ObjIsRequestUser',
    'IsFromUser',
    'IsUserOrReadOnly',
    'IsCompanyUser',
)


class ObjIsRequestUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsFromUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.from_user == request.user


class IsUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class IsCompanyUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.type == User.TYPE_COMPANY
