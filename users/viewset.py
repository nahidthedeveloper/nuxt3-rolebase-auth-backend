from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from users.serializer import UserSerializer
from authentication.models import Account
from rest_framework import status
from django.contrib.auth.models import Permission


class UserViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = UserSerializer

    # permission_classes = [IsAdminUser]

    def list(self, request, *args, **kwargs):
        # self.permissions = self.check_permissions(request)
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='authentication_permissions')
    def permissions(self, request):
        permissions = [
            {"id": perm.id, "name": f"{perm.content_type.app_label}.{perm.codename}"}
            for perm in Permission.objects.filter(content_type__app_label='authentication')
        ]
        return Response({"permissions": permissions}, status=status.HTTP_200_OK)
