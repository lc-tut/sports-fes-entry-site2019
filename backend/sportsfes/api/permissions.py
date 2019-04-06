from rest_framework import permissions


class DoesRequestUserOwnTeam(permissions.BasePermission):
    """
    Only user who created the team can edit, delete the information
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.created_by == request.user


class DoesRequestUserOwnTeamOneBelongs(permissions.BasePermission):
    """
    Only user who created the team can view, create, edit, delete the member belongs the team.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.team.created_by == request.user