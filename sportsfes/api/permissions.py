from rest_framework import permissions


class HasUserIdInSessionForTeam(permissions.BasePermission):
    """
    Custom permission for token sign in
    """

    def has_object_permission(self, request, view, obj):

        return request.user.is_authenticated