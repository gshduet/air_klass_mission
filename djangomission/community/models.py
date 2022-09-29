from email.policy import default
from django.db import models

from core.models import TimeStampModel


class Question(TimeStampModel):
    klass = models.ForeignKey(
        'contentshub.Klass', on_delete=models.CASCADE, verbose_name='질문이 올라온 강의')
    student = models.ForeignKey(
        'account.User', on_delete=models.PROTECT, verbose_name='질문자')
    contents = models.TextField(verbose_name='질문내용')
    is_answered = models.BooleanField(default=False, verbose_name='답변 여부')
    is_deleted = models.BooleanField(default=False, verbose_name='질문 삭제여부')
    deleted_at = models.DateTimeField(auto_now=True, verbose_name='질문 삭제시각')

    class Meta:
        db_table = 'question'
        ordering = (-'created_at')

    def __str__(self):
        return f'{self.klass}-{self.student}'


class Answer(TimeStampModel):
    klass = models.ForeignKey(
        'contentshub.Klass', on_delete=models.CASCADE, verbose_name='질문이 올라온 강의')
    question = models.OneToOneField('Qeustion', verbose_name='답변이 달릴 강의')
    contents = models.TextField(verbose_name='답변내용')
    is_deleted = models.BooleanField(default=False, verbose_name='질문 삭제여부')
    deleted_at = models.DateTimeField(auto_now=True, verbose_name='질문 삭제시각')

    class Meta:
        db_table = 'answer'
        ordering = (-'created_at')

    def __str__(self):
        return f'{self.klass}-{self.question}'
