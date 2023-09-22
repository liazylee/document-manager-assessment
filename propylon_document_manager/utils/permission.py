from rest_framework import permissions


class OwnFilePermission(permissions.BasePermission):
    """
    Object-level permission to only allow own files
    """
    def has_object_permission(self, request, view, obj):
        # obj here is a UserFile instance
        return obj.file_user == request.user
