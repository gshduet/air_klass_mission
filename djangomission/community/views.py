from datetime import datetime

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from community.serializers import Question, Answer
from community.serializers import QuestionSerializer, QuestionDetailSerializer
from accounts.models import User
from contentshub.models import Master, Klass


class QuestionView(APIView):
    queryset = Question.objects.all()

    def post(self, request: Request, klass_id: int) -> Response:
        """
        특정 강의에 질문을 남기는 API
        로그인 하지 않을 경우 에러 반환
        """
        if 'access_token' not in request.COOKIES:
            return Response(
                {'MESSAGE': 'NEED_AUTHORIZATION.PLEASE_SIGN_IN'}, status=status.HTTP_401_UNAUTHORIZED
            )

        klass = Klass.objects.get(id=klass_id)
        user = User.objects.get(email=request.COOKIES['user'])
        serializer = QuestionSerializer(data=request.data)

        if serializer.is_valid():
            Question.objects.create(
                klass=klass, student=user, contents=request.data['contents']
            )
            return Response({'MESSAGE': 'SUCCESS'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request: Request, klass_id: int) -> Response:
        """
        특정 강의에 남겨진 질문들을 리스트로 뽑아오는 API
        로그인 하지 않아도 조회 가능
        삭제되지 않은 질문만 조회 됨
        """
        try:
            klass = Klass.objects.get(id=klass_id)
            question = Question.objects.filter(klass=klass, is_deleted=False)
            serializer = QuestionSerializer(question, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Klass.DoesNotExist:
            return Response({'MESSAGE': 'KLASS_DOES_NOT_EXISTS'}, status=status.HTTP_404_NOT_FOUND)


class QuestionDetailView(APIView):

    def get(self, request: Request, klass_id: int, question_id: int) -> Response:
        """
        특정 질문의 상세정보를 조회하는 API
        삭제되지 않은 질문만 조회 됨
        """
        try:
            question = Question.objects.get(id=question_id)
            if question.is_deleted:
                return Response({'MESSAGE': 'QUESTION_DOES_NOT_EXISTS'}, status=status.HTTP_404_NOT_FOUND)

            serializer = QuestionDetailSerializer(question)
            print(serializer)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Question.DoesNotExist:
            return Response({'MESSAGE': 'QUESTION_DOES_NOT_EXISTS'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request: Request, klass_id: int, question_id: int) -> Response:
        """
        특정 질문의 상세정보를 수정하는 API
        질문 내용, 질문 작성자, 질문을 남긴 강의에 대한 정보 반환
        해당 질문을 작성한 작성자가 아닐 시 에러 반환
        """
        try:
            user = User.objects.get(email=request.COOKIES['user'])
            question = Question.objects.get(id=question_id)

            if user != question.student:
                return Response({'MESSAGE': 'UNAUTHORIZED_USER'}, status=status.HTTP_403_FORBIDDEN)

            serializer = QuestionDetailSerializer(
                question, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Question.DoesNotExist:
            return Response({'MESSAGE': 'QUESTION_DOES_NOT_EXISTS'}, status=status.HTTP_404_NOT_FOUND)


    def delete(self, request: Request, klass_id: int, question_id: int) -> Response:
        """
        특정 질문을 삭제하는 API

        질문 이력 확보를 위해 삭제 요청이 들어올 경우 DB에서 바로 삭제하는 것이 아닌 
        id_delete 플래그를 True 혹은 False로 변환하며
        이를 바탕으로 False일 경우 삭제되지 않은 질문, True일 경우 삭제된 질문으로 구분하며
        조회 시 False인 질문만 조회 가능

        is_answered 플래그를 바탕으로 질문이 되었는지를 확인하며
        만약 is_answered가 True일 경우 삭제할 수 없음
        """
        question = Question.objects.select_related('klass').get(id=question_id)
        user = User.objects.get(email=request.COOKIES['user'])

        if user != question.student:
            return Response({'MESSAGE': 'UNAUTHORIZED_USER'}, status=status.HTTP_403_FORBIDDEN)

        elif question.klass.master == user.master:
            pass

        try:
            if question.is_answered == False:
                question.is_deleted = True
                question.deleted_at = datetime.now()
                question.save()

                return Response({'MESSAGE': 'DELETE_SUSSECED'}, status=status.HTTP_204_NO_CONTENT)

            else:
                return Response({'MESSAGE': 'CAN_NOT_DELETE.ANSWER_ALREADY_WRITTEN'}, status=status.HTTP_204_NO_CONTENT)

        except Question.DoesNotExist:
            return Response({'MESSAGE': 'QUESTION_DOES_NOT_EXISTS'}, status=status.HTTP_404_NOT_FOUND)


