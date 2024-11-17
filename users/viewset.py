from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Permission
from authentication.models import Account
from authentication.serializer import SignupSerializer
from users.serializer import UserSerializer
from rest_framework.exceptions import MethodNotAllowed
from users.permissions import CanViewUsers, CanChangeUsers, CanDeleteUsers, CanAddUsers


class UserViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()

    def get_permissions(self):
        if self.action == "list":
            return [CanViewUsers()]
        # elif self.action == "update":
        #     return [CanChangeUsers()]
        elif self.action == "destroy":
            return [CanDeleteUsers()]
        elif self.action == "create":
            return [CanAddUsers()]
        elif self.action == "authentication_permissions":
            return [IsAuthenticated()]
        elif self.action == "login_user_permissions":
            return [IsAuthenticated()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == "create":
            return SignupSerializer
        return UserSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "User created successfully."}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        if request.method != "PATCH":
            raise MethodNotAllowed("Only PATCH method is allowed for updates.")
        
        if not request.user.has_perm('authentication.change_account') or not request.user.is_superuser:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "User updated successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.id == request.user.id:
            return Response(
                {"detail": "You cannot delete your own account."},
                status=status.HTTP_403_FORBIDDEN,
            )
        instance.delete()
        return Response({"detail": "User deleted successfully."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"], url_path="authentication_permissions")
    def authentication_permissions(self, request):
        permissions = Permission.objects.filter(content_type__app_label="authentication")
        data = [{"id": perm.id, "name": perm.codename} for perm in permissions]
        return Response({"permissions": data}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"], url_path="login_user_permissions")
    def login_user_permissions(self, request):
        user_permissions = request.user.user_permissions.all()
        data = [
            {"id": perm.id, "name": f"{perm.content_type.app_label}.{perm.codename}"}
            for perm in user_permissions
        ]
        return Response({"user_permissions": data}, status=status.HTTP_200_OK)
