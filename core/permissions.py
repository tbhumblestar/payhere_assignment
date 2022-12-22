from rest_framework import permissions


class IsAdminOrIsWriterOrForbidden(permissions.BasePermission):
    def has_permission(self, request, view):
        is_authenticated = bool(request.user and request.user.is_authenticated)

        return is_authenticated

    def has_object_permission(self, request, view, obj):

        is_staff = bool(request.user.is_staff)
        is_writer = bool(request.user == obj.user)

        return is_staff or is_writer
