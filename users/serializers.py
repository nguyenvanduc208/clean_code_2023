from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255)


class UpdateUserSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, required=False)
    email = serializers.EmailField(max_length=100)
    email_verified_at = serializers.CharField(max_length=100, required=False)
    is_admin = serializers.CharField(max_length=100)


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "username", "password"]