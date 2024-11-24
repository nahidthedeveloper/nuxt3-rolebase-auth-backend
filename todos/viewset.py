from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Todos
from .serializer import TodosSerializer
from .permissions import CanViewTodos, CanChangeTodos, CanDeleteTodos, CanAddTodos
from rest_framework import status


class TodosView(viewsets.ModelViewSet):
    queryset = Todos.objects.all()
    serializer_class = TodosSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == "create":
            return [CanAddTodos()]
        elif self.action == "list" or self.action == "retrieve":
            return [CanViewTodos()]
        elif self.action == "update" or self.action == "partial_update":
            return [CanChangeTodos()]
        elif self.action == "destroy":
            return [CanDeleteTodos()]
        return [CanViewTodos()]

    def get_queryset(self):
        return Todos.objects.filter(user=self.request.user).order_by('-created_at')

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
        super().update(request, *args, **kwargs)  # Perform the update
        return Response({'detail': 'Todo updated successfully.'}, status=200)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            raise PermissionDenied("You do not have permission to delete this Todo.")
        super().destroy(request, *args, **kwargs)  # Perform the delete
        return Response({'detail': 'Todo deleted successfully.'}, status=200)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"detail": "Todo added successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400)
