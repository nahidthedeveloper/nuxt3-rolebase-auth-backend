from rest_framework.permissions import BasePermission


class IsSuperuserOrHasPermission(BasePermission):
    def __init__(self, permission_codename):
        self.permission_codename = permission_codename

    def has_permission(self, request, view):
        return (
            request.user.is_superuser or
            request.user.has_perm(self.permission_codename)
        )


class CanViewUsers(IsSuperuserOrHasPermission):
    def __init__(self):
        super().__init__("authentication.view_account")


class CanChangeUsers(IsSuperuserOrHasPermission):
    def __init__(self):
        super().__init__("authentication.change_account")


class CanDeleteUsers(IsSuperuserOrHasPermission):
    def __init__(self):
        super().__init__("authentication.delete_account")


class CanAddUsers(IsSuperuserOrHasPermission):
    def __init__(self):
        super().__init__("authentication.add_account")

