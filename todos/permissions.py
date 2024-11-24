from rest_framework.permissions import BasePermission


class IsSuperuserOrHasPermission(BasePermission):
    def __init__(self, permission_codename):
        self.permission_codename = permission_codename

    def has_permission(self, request, view):
        return (
            request.user.is_superuser or
            request.user.has_perm(self.permission_codename)
        )


class CanViewTodos(IsSuperuserOrHasPermission):
    def __init__(self):
        super().__init__("todos.view_todos")


class CanChangeTodos(IsSuperuserOrHasPermission):
    def __init__(self):
        super().__init__("todos.change_todos")


class CanDeleteTodos(IsSuperuserOrHasPermission):
    def __init__(self):
        super().__init__("todos.delete_todos")


class CanAddTodos(IsSuperuserOrHasPermission):
    def __init__(self):
        super().__init__("todos.add_todos")

