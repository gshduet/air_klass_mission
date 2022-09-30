import json

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .serializers import SignUpSerializer


class SignUpView(APIView):
    permissions_classes = [AllowAny]
    serializer_class = SignUpSerializer

    def post(self, request) -> Response:

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response({'MESSAGE': 'SIGN_UP_SUCCESS'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignInView(APIView):

    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        password = data['password']
        user = authenticate(email=email, password=password)

        if user:
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)

            return Response(
                {
                    'MESSAGE': 'SIGN_IN_SUCCESS',
                    'ACCESS_TOKEN': access_token,
                    'REFRESH_TOKEN': refresh_token
                },
                status=status.HTTP_200_OK
            )

        else:
            return Response({'MESSAGE': 'INVALID_EMAIL_OR_PASSWORD'}, status=status.HTTP_400_BAD_REQUEST)