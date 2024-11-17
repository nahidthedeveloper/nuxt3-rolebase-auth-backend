from authentication.models import Account
from rest_framework import serializers
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class EmptySerializer(serializers.Serializer):
    pass


class SignupSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = ['username', 'email', 'password', 'confirm_password', 'role']

    def validate(self, attrs):
        if Account.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({'email': 'User already exists with this email'})

        if Account.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({'username': 'Username is already taken'})

        if len(attrs['password']) < 8:
            raise serializers.ValidationError({"password": "Password must be more than 8 characters."})

        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})

        if not attrs['role']:
            raise serializers.ValidationError({"role": "Must select user role."})

        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = Account.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username_or_email = attrs.get('username_or_email')
        password = attrs.get('password')

        # Determine if input is an email or username
        user = None
        try:
            validate_email(username_or_email)
            user = Account.objects.filter(email=username_or_email).first()
        except ValidationError:
            user = Account.objects.filter(username=username_or_email).first()

        if not user or not user.check_password(password):
            raise serializers.ValidationError({'password': 'Username/Email or password is incorrect'})

        if not user.is_active:
            raise serializers.ValidationError({'username_or_email': 'This account is inactive.'})

        attrs['user'] = user
        return attrs
