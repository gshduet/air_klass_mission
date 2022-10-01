import json

from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Klass
from .serializers import KlassCreateSerializer
from .permission import IsMasterUser
from accounts.models import User


@method_decorator(csrf_exempt, name='dispatch')
class SetMasterView(View):

    def post(self, request):
        """
        강사 권한 부여 API
        어드민 권한을 가진 사람이 어드민 페이지에서 직접 지정하거나 비공개 엔드포인트를 통해 지정할 수 있도록 설계
        """
        data = json.loads(request.body)
        email = data['email']
        new_master = User.objects.get(email=email)
        master_name = data.get('master_name', new_master.username)
        description = data.get('description', None)

        new_master.is_master = True
        new_master.save()

        _, is_created = Master.objects.get_or_create(
            user=new_master, master_name=master_name, description=description
        )

        if not is_created:
            return JsonResponse({'MESSAGE': 'ALREADY_HAVE_PERMISSION'}, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse({'MESSAGE': 'SET_MASTER_SUCCESS'}, status=status.HTTP_201_CREATED)

    def delete(self, request):
        """
        강사자격 삭제 API
        어드민 권한을 가진 사람이 어드민 페이지에서 직접 권한을 삭제하거나, 비공개 엔드포인트를 통해 지정할 수 있도록 설계
        """
        data = json.loads(request.body)
        email = data['email']

        if not User.objects.filter(email=email, is_master=True).exists():
            return JsonResponse({'MESSAGE': 'ALREADY_UNSET_MASTER_PERMISSION'}, status=status.HTTP_403_FORBIDDEN)

        master = User.objects.get(email=email)
        master.master.delete()
        master.is_master = False
        master.save()

        return JsonResponse({'MESSAGE': 'UNSET_MASTER_SUCCESS'}, status=status.HTTP_204_NO_CONTENT)


class KlassCreateView(generics.CreateAPIView):
    queryset = Klass.objects.all()
    serializer_class = KlassCreateSerializer
    permission_classes = [IsMasterUser]

    def post(self, request):
        serializer = KlassCreateSerializer(data=request.data)
        if serializer.is_valid():
            Klass.objects.create(
                master = request.user.master,
                title = request.data['title'],
                description = request.data['description'],
            )
        
            return Response({'MESSAGE': 'SUCCESS'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)