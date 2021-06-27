from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView

from users.serializers import UserSerializer
from users.models import CustomUser


class UserLCView(ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects


class UserRUDView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects
    lookup_field = 'id'


class UserDetailsView(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects

    def get_object(self):
        user = self.request.user
        return self.queryset.filter(id=user.id).first()
