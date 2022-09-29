from tabnanny import verbose
from django.db import models


class Master(models.Model):
    user = models.OneToOneField(
        'account.User', on_delete=models.CASCADE, verbose_name='강사 자격 신청자')
    master_name = models.CharField(max_length=20, verbose_name='강사로서의 이름')
    description = models.TextField(verbose_name='강사 설명')

    class Meta:
        db_table = 'master'

    def __str__(self):
        return f'{self.master_name}'


class Klass(models.Model):
    master = models.ForeignKey(
        'Master', on_delete=models.CASCADE, verbose_name='강사 이름')
    title = models.CharField(max_length=50, verbose_name='강의 제목')
    description = models.TextField(verbose_name='강의 설명')

    class Meta:
        db_table = 'klass'

    def __str__(self):
        return f'{self.title}'
