from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny

from .serializers import CreateGameSerializer
from .serializers import ProfileSerializer
from .serializers import UserSerializer

User = get_user_model()


class ProfileView(RetrieveAPIView):
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user


class SignupView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    permission_classes = [AllowAny]


class CreateGameView(CreateAPIView):
    serializer_class = CreateGameSerializer
