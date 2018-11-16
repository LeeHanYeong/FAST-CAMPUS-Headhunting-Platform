from rest_framework import permissions


class ObjIsRequestUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsFromUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.from_user == request.user
