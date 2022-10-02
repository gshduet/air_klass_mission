from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from contentshub.models import Master, Klass
from contentshub.serializers import MasterSerializer, KlassSerializer, KlassDetailSerializer
from accounts.models import User


class MasterView(APIView):

    def post(self, request: Request) -> Response:
        """
        특정 유저에게 강사 권한을 부여하는 API
        """
        serializer = MasterSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = User.objects.get(email=request.COOKIES['user'])
            master_name = request.data.get('master_name', user.username)
            description = request.data.get('description', None)

            user.is_master = True
            user.save()

            _, is_created = Master.objects.get_or_create(
                user=user, master_name=master_name, description=description
            )
            if not is_created:
                return Response({'MESSAGE': 'ALREADY_HAVE_PERMISSION'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'MESSAGE': 'SET_MASTER_SUCCESS'}, status=status.HTTP_201_CREATED)

    def delete(self, request: Request) -> Response:
        """
        특정 유저에게 부여된 강사 권한을 해제하는 API
        """
        master = User.objects.get(email=request.COOKIES['user'])

        if not master.is_master:
            return Response({'MESSAGE': 'ALREADY_UNSET_MASTER_PERMISSION'}, status=status.HTTP_403_FORBIDDEN)

        master.master.delete()
        master.is_master = False
        master.save()

        return Response({'MESSAGE': 'UNSET_MASTER_SUCCESS'}, status=status.HTTP_204_NO_CONTENT)


class KlassView(APIView):
    queryset = Klass.objects.all()

    def post(self, request: Request) -> Response:
        """
        특정 강사가 강의를 개설하는 API
        강사권한이 없는 유저가 개설 시도 시 에러 반환
        """
        user = User.objects.get(email=request.COOKIES['user'])
        serializer = KlassSerializer(data=request.data)

        if not user.is_master:
            return Response({'MESSAGE': 'UNAUTHORIZED_USER'}, status=status.HTTP_403_FORBIDDEN)

        if serializer.is_valid():
            Klass.objects.create(
                master=user.master,
                title=request.data['title'],
                description=request.data['description'],
            )

            return Response({'MESSAGE': 'SUCCESS'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, reqeust: Request) -> Response:
        """
        강의 전체 리스트를 반환하는 API
        """
        klass = Klass.objects.all()
        serializer = KlassDetailSerializer(klass, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class KlassDetailView(APIView):

    def get(self, request: Request, klass_id: int) -> Response:
        """
        특정 강의의 상세 정보를 조회하는 API
        """
        try:
            klass = Klass.objects.get(id=klass_id)
            serializer = KlassDetailSerializer(klass)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Klass.DoesNotExist:
            return Response({'MESSAGE': 'KLASS_DOES_NOT_EXISTS'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request: Request, klass_id: int) -> Response:
        """
        특정 강의의 상세정보를 수정하는 API
        해당 강의를 개설한 강사가 아닐 시 에러 반환
        """
        user = User.objects.get(email=request.COOKIES['user'])
        klass = Klass.objects.get(id=klass_id)

        if user != klass.master:
            return Response({'MESSAGE': 'UNAUTHORIZED_USER'}, status=status.HTTP_403_FORBIDDEN)

        serializer = KlassDetailSerializer(
            klass, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
