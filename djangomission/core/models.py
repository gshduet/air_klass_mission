from django.db import models


class TimeStampModel(models.Model):
    """
    데이터 생성 및 수정 이력 관리를 위한 모델
    주로 서비스에 직접 사용될 테이블에 상속하여 사용할 예정
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='데이터 생성시각')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='마지막 데이터 변경시각')

    class Meta:
        abstract = True
