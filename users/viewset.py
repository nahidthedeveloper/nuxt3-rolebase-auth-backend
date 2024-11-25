from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import Permission
from authentication.models import Account
from authentication.serializer import SignupSerializer
from users.serializer import UserSerializer



class UserViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()

    def get_permissions(self):
        if self.action in ["create", "list", "retrieve", "update", "partial_update", "destroy"]:
            return [IsAdminUser()]
        elif self.action == "permissions":
            return [IsAuthenticated()]
        elif self.action == "user_permissions":
            return [IsAuthenticated()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == "create":
            return SignupSerializer
        return UserSerializer

    def list(self, request, *args, **kwargs):
        queryset = Account.objects.exclude(is_superuser=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "User created successfully."}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "User updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "User deleted successfully."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"], url_path="permissions")
    def permissions(self, request):
        permissions = Permission.objects.filter(content_type__app_label="todos")
        data = [
            {"id": perm.id, "name": f"{perm.content_type.app_label}.{perm.codename}"}
            for perm in permissions
        ]
        return Response({"permissions": data}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"], url_path="user_permissions")
    def user_permissions(self, request):
        user_permissions = request.user.user_permissions.all()
        data = [
            {"id": perm.id, "name": f"{perm.content_type.app_label}.{perm.codename}"}
            for perm in user_permissions
        ]
        return Response({"user_permissions": data}, status=status.HTTP_200_OK)
