from rest_framework import serializers

from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = "__all__"
        extra_kwargs = {
            'password': {'write_only': True},
            'groups': {'write_only': True},
            'group_permissions': {'write_only': True},
        }

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
