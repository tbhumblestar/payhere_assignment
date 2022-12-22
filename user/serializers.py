from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)


class CustomTokenObtainPairTokenSerializer(TokenObtainPairSerializer):
    """Create"""

    def validate(self, attrs):
        res = super().validate(attrs)
        res["email"] = attrs.get("email")
        return res
