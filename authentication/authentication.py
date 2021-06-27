from rest_framework.authentication import TokenAuthentication
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions

from authentication.models import UserTokenModel
from authentication.service_utils import UserUtils


class CustomAuthentication(TokenAuthentication):
    model = UserTokenModel

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token: UserTokenModel = model.objects.get(key=key)
            if not token.is_valid:
                raise exceptions.AuthenticationFailed(_('Token Expired. Please Login Again'))
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))
        user = UserUtils.get_user_by_id(token.user_id)
        if not user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        return user, token
