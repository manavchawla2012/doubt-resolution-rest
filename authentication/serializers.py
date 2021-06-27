from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import ugettext as _

from authentication.models import UserTokenModel


class PasswordField(serializers.CharField):

    def __init__(self, **kwargs):
        if 'style' not in kwargs:
            kwargs['style'] = {'input_type': 'password'}
        else:
            kwargs['style']['input_type'] = 'password'
        super(PasswordField, self).__init__(**kwargs)


class LoginSerializer(serializers.Serializer):
    token = serializers.CharField(read_only=True)

    def __init__(self, *args, **kwargs):
        """
        Dynamically add the USERNAME_FIELD to self.fields.
        """
        super(LoginSerializer, self).__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField(write_only=True)
        self.fields['password'] = PasswordField(write_only=True)

    def get_username_field(self):
        from django.contrib.auth import get_user_model
        try:
            username_field = get_user_model().USERNAME_FIELD
        except:
            username_field = 'username'

        return username_field

    @property
    def username_field(self):
        return self.get_username_field()

    def validate(self, attrs):
        credentials = {
            self.username_field: attrs.get(self.username_field),
            'password': attrs.get('password')
        }

        if all(credentials.values()):
            user = authenticate(**credentials)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg)

                return {
                    "user": user
                }
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "{username_field}" and "password".')
            msg = msg.format(username_field=self.username_field)
            raise serializers.ValidationError(msg)

    def create(self, validated_data):
        user = validated_data.get("user")
        user_token_object = UserTokenModel.objects.filter(user_id=user.id, is_valid=True).first()
        if not user_token_object:
            user_token_object: UserTokenModel = UserTokenModel(user_id=user.id, is_valid=True)
            user_token_object.save()

        return {
            "token": user_token_object.key
        }