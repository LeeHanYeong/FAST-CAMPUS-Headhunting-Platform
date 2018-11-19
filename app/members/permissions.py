from rest_framework import permissions


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
