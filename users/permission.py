from rest_framework import permissions


class CreateUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('authentication.add_account')


class ViewUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('authentication.view_permissions')


class UpdateUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('authentication.change_account')


class DeleteUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('authentication.delete_account')
