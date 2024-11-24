from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Todos
from .serializer import TodosSerializer
from .permissions import CanViewTodos, CanChangeTodos, CanDeleteTodos, CanAddTodos

class TodosView(viewsets.ModelViewSet):
    queryset = Todos.objects.all()
    serializer_class = TodosSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ["create"]:
            return [CanAddTodos()]
        elif self.action in ["list", "retrieve"]:
            return [CanViewTodos()]
        elif self.action in ["update", "partial_update"]:
            return [CanChangeTodos()]
        elif self.action == "destroy":
            return [CanDeleteTodos()]
        return [CanViewTodos()]

    def get_queryset(self):
        return Todos.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            raise PermissionDenied("You do not have permission to access this Todo.")
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            raise PermissionDenied("You do not have permission to update this Todo.")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            raise PermissionDenied("You do not have permission to delete this Todo.")
        return super().destroy(request, *args, **kwargs)
