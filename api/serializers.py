from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = serializers.ALL_FIELDS

        extra_kwargs = {
            'password': {
                'validators': [validate_password],
                'write_only': True,
            },
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class ProfileSerializer(UserSerializer):
    class Meta:
        model = User
        exclude = ['password']
