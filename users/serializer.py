from rest_framework import serializers
from authentication.models import Account


class UserSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ['id', 'username', 'email', 'role', 'permissions']

    def get_permissions(self, obj):
        permissions = obj.user_permissions.all()
        return [
            {
                "id": perm.id,
                "name": f"{perm.content_type.app_label}.{perm.codename}"
            }
            for perm in permissions
        ]

    def update(self, instance, validated_data):
        permissions_data = validated_data.pop('permissions', None)

        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.role = validated_data.get('role', instance.role)
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        instance.save()

        if permissions_data is not None:
            instance.user_permissions.set(permissions_data)

        return instance
