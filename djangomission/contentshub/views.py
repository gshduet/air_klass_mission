from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Master
from .serializers import SetMasterSerializer
from accounts.models import User


class SetMasterView(APIView):
    serializer_class = SetMasterSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)

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
        master = User.objects.get(email=request.COOKIES['user'])

        if not master.is_master:
            return Response({'MESSAGE': 'ALREADY_UNSET_MASTER_PERMISSION'}, status=status.HTTP_403_FORBIDDEN)

        master.master.delete()
        master.is_master = False
        master.save()

        return Response({'MESSAGE': 'UNSET_MASTER_SUCCESS'}, status=status.HTTP_204_NO_CONTENT)


class KlassView(APIView):
    
    def post(self, request: Request) -> Response:
        ...
