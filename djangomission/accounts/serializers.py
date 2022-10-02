import datetime

from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'password', 'username']

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        username = validated_data['username']

        if User.objects.filter(email=email).exists():
            return serializers.ValidationError('ALREADY_EXISTS_EMAIL')

        new_user = User.objects.create_user(
            email=email,
            password=password,
            username=username
        )

        return new_user


class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, data):
        email = data['email']
        password = data['password']

        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError('INVALID_EMAIL_OR_PASSWORD')

        else:
            token = RefreshToken.for_user(user)
            refresh_token = str(token)
            access_token = str(token.access_token)

            return {'user': user, 'refresh_token': refresh_token, 'access_token': access_token}
