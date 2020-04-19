from django.contrib.auth import get_user_model
from rest_framework import serializers

from account.models import UserProfile


class AuthUserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = read_only_fields = (
            "username",
            "is_staff",
            "is_active",
        )


class AuthUserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = read_only_fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "is_staff",
            "is_active",
            "last_login",
            "date_joined"
        )


class UserProfileListSerializer(serializers.ModelSerializer):
    auth_user = AuthUserListSerializer()

    class Meta:
        model = UserProfile
        fields = read_only_fields = (
            "public_id",
            "auth_user"
        )


class UserProfileDetailSerializer(serializers.ModelSerializer):
    auth_user = AuthUserDetailSerializer()

    class Meta:
        model = UserProfile
        fields = read_only_fields = (
            "public_id",
            "auth_user"
        )
