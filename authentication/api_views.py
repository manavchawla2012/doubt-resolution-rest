from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.settings import api_settings

from authentication.serializers import LoginSerializer
from authentication.models import UserTokenModel


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    authentication_classes = []
    permission_classes = []

    def post(self, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class VerifyAuthView(GenericAPIView):

    def post(self, *args, **kwargs):
        return Response({
            "status": "verified"
        })


class LogoutView(GenericAPIView):

    def post(self, *args, **kwargs):
        user = self.request.user
        user_active_token = UserTokenModel.objects.filter(user_id=user.id, is_valid=True).first()
        user_active_token.is_valid = False
        user_active_token.save()
        return Response({
            "msg": "Successfully Logged Out"
        })
