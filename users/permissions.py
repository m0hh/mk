from rest_framework import permissions


class UpdatePermission(permissions.BasePermission):

    edit_methods = ("PUT", "PATCH")

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if obj.users == request.user.info:
            return True

        return False

class ModeerPermission(permissions.BasePermission):

    edit_methods = ("POST",)

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.user.info.rank == "CEO" or request.user.info.rank == "CTO":
            return True

        return False