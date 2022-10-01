import datetime

from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class SignUpSerializer(serializers.ModelSerializer):
    """
    회원가입을 위한 Serializer
    회원가입 시 email, passwork, username 항목을 요구하며
    email 중복여부를 확인하고 email 형식에 대한 유효성 검사를 진행함
    """

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
    """
    로그인을 위한 Serializer
    django_restframework_jwt는 19년 이후로 업데이트를 중단했기 때문에
    DRF 공식문서에서 권장하는 django_restframework_simplejwt를 통해 인증/인가를 포함한 SignIn 기능을 구현
    """
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
            return serializers.ValidationError('INVALID_EMAIL_OR_PASSWORD')

        else:
            token = RefreshToken.for_user(user)
            refresh_token = str(token)
            access_token = str(token.access_token)

            return {'user': user, 'refresh_token': refresh_token, 'access_token': access_token}
