from rest_framework import serializers
from authentication.models import Account
from django.contrib.auth.models import Permission

class UserSerializer(serializers.ModelSerializer):
    permissions = serializers.ListField(child=serializers.IntegerField(), required=False)

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
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        permissions = instance.user_permissions.all()
        representation['permissions'] = [{
                "id": perm.id,
                "name": f"{perm.content_type.app_label}.{perm.codename}"
            } for perm in permissions]
        
        return representation

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

            permissions = Permission.objects.filter(id__in=permissions_data)
            if permissions.count() == len(permissions_data):
                instance.user_permissions.set(permissions)
            else:
                invalid_permissions = set(permissions_data) - set(permissions.values_list('id', flat=True))
                raise serializers.ValidationError(f"Some permissions are invalid: {', '.join(map(str, invalid_permissions))}")

        return instance
