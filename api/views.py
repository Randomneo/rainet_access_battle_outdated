from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveAPIView

from .serializers import ProfileSerializer

User = get_user_model()


class ProfileView(RetrieveAPIView):
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user
