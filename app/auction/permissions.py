from rest_framework import permissions


class IsReadyOnlyRequest(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsLotObjectOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.lot.user.auth_user == request.user
