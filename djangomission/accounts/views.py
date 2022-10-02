from django.contrib.auth import login, logout
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from .serializers import SignUpSerializer, SignInSerializer
from .models import User


class SignUpView(APIView):
    permissions_classes = [AllowAny]
    serializer_class = SignUpSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response({'MESSAGE': 'SIGN_UP_SUCCESS'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignInView(APIView):
    permissions_classes = [AllowAny]
    serializer_class = SignInSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            response = Response(
                {
                    'MESSAGE': 'SIGN_IN_SUCCESS',
                }, status=status.HTTP_200_OK)

            response.set_cookie('user', serializer.validated_data['user'])
            response.set_cookie(
                'access_token', serializer.validated_data['access_token'])
            response.set_cookie(
                'refresh_token', serializer.validated_data['refresh_token'])

            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request) -> Response:
        response = Response(
                {
                    'MESSAGE': 'SIGN_OUT_SUCCESS',
                }, status=status.HTTP_202_ACCEPTED)
        
        response.delete_cookie('user')
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')

        return response