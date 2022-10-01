import json

from django.contrib.auth import login
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import SignUpSerializer, SignInSerializer


class SignUpView(APIView):
    """
    회원가입 API
    email, password, username 항목을 입력받은 후
    email 유효성 검사, 중복여부 검사를 진행 해 해당 사항 없으면 회원가입 후 201 status code 반환
    """
    permissions_classes = [AllowAny]
    serializer_class = SignUpSerializer

    def post(self, request) -> Response:
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response({'MESSAGE': 'SIGN_UP_SUCCESS'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignInView(APIView):
    """
    로그인 API
    email과 password 항목을 입력받은 후 DB에 존재하는 정보와 일치할 경우
    해당 유저에 대한 정보를 토대로 refresh_token과 access_token을 발급
    클라이언트에게 전달하여 클라이언트의 쿠키 혹은 로컬스토리지 등에 보관
    우선은 로컬스토리지에 저장하며 
    로그인 후 보내는 요청마다 header에 access_token을 담아 같이 전송한다고 가정
    """
    permissions_classes = [AllowAny]
    serializer_class = SignInSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            login(request, serializer.validated_data['sign_in_user'])
            response = Response({'MESSAGE': 'SIGN_IN_SUCCESS'}, status=status.HTTP_200_OK)
            response.set_cookie('user', serializer.validated_data['sign_in_user'].id)
            response.set_cookie('is_master', serializer.validated_data['sign_in_user'].is_master)
            response.set_cookie('access_token', serializer.validated_data['access_token'])
            response.set_cookie('refresh_token', serializer.validated_data['refresh_token'])

            return response

    # def post(self, request):
    #     data = json.loads(request.body)
    #     email = data['email']
    #     password = data['password']
    #     user = authenticate(email=email, password=password)

    #     if user:
    #         token = TokenObtainPairSerializer.get_token(user)
    #         refresh_token = str(token)
    #         access_token = str(token.access_token)

    #         return Response(
    #             {
    #                 'MESSAGE': 'SIGN_IN_SUCCESS',
    #                 'ACCESS_TOKEN': access_token,
    #                 'REFRESH_TOKEN': refresh_token
    #             },
    #             status=status.HTTP_200_OK
    #         )

    #     else:
    #         return Response({'MESSAGE': 'INVALID_EMAIL_OR_PASSWORD'}, status=status.HTTP_400_BAD_REQUEST)