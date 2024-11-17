from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from authentication.serializer import SignupSerializer, LoginSerializer, EmptySerializer


class AuthenticationViewSet(viewsets.ModelViewSet):
    serializer_class = []
    queryset = []

    def get_serializer_class(self):
        if self.action == 'signup':
            return SignupSerializer
        elif self.action == 'login':
            return LoginSerializer
        return EmptySerializer

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'], url_path='signup')
    def signup(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Signup successfully'}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['POST'], url_path='login')
    def login(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            user.last_login = timezone.now()
            user.save()
            refresh = RefreshToken.for_user(user)

            return Response({
                'token': str(refresh.access_token),
                'email': user.email,
                'id': user.id,
                'name': user.name,
                'role': user.role,
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
